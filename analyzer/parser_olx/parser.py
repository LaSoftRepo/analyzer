import datetime
import json

from django.core.mail import send_mail
from django.template.loader import render_to_string
from lxml import html
import re
import requests
from requests import cookies
from urllib.parse import urljoin

from django.utils import timezone
from django.utils.timezone import make_naive

from collection.models import Collections, Donor
from users.models import User


class ConfigParserOlx:
    main_link = 'https://www.olx.ua/transport/legkovye-avtomobili/' \
                'q-%D0%B4%D1%82%D0%BF/?' \
                'search[filter_float_price%3Afrom]=25000&' \
                'search[filter_float_price%3Ato]=125000&' \
                'search[filter_float_motor_year%3Afrom]=1990'

    SELECTOR_GETLINK_ARTICLES = '//a[@class="marginright5 link linkWithHash detailsLink"]/@href'  # noqa
    SELECTOR_DATE = '//div[@class="offer-titlebox__details"]//em/text()'
    SITE_URL = 'http://olx.ua'
    AJAX_PHONE = '/ajax/misc/contact/phone/'
    ID = '//div[@class="offer-titlebox__details"]//em//small//text()'
    LOCATION = '//div[@class="offer-titlebox__details"]//a[@class="show-map-link"]//strong//text()'  # noqa
    TITLE = '//div[@class="offer-titlebox"]//h1//text()'
    DESCRIPTION = '//div[@class="clr"]//p[@class="pding10 lheight20 large"]//text()'  # noqa
    PRICE = '//div[@class="price-label"]//strong/text()'
    NAME = '//div[@class="offer-user__details"]//h4//a//text()'


class Requester(object):

    def __init__(self, link, ssid=None):
        self.link = link

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/41.0.2228.0 Safari/537.36'}

        self.response = requests.get(self.link, headers=headers,
                                     cookies=self._get_cookies(ssid))
        try:
            self.PHPSESSID = self.response.cookies['PHPSESSID']
        except KeyError:
            pass
        self.parsed_body = html.fromstring(self.response.text)

    def get_link(self, selector):
        list_link = self.parsed_body.xpath(selector)
        list_link = \
            [urljoin(self.response.url, url)for url in list_link]
        return list_link

    def get_text(self, selector='//text()'):
        return self.parsed_body.xpath(selector)

    @staticmethod
    def _get_cookies(ssid):
        jar = requests.cookies.RequestsCookieJar()
        jar.set('PHPSESSID', ssid, domain='.olx.ua', path='/')
        return jar


class ParserOlx(ConfigParserOlx):

    def __init__(self):
        self.page = '1'
        self.stop_parse = 0
        self.emails_admin = User.objects.filter(
            is_get_email=True).values_list('email', flat=True)

    @property
    def stop_day(self):
        return timezone.now() - datetime.timedelta(days=7)

    def run(self):
        for i, page in enumerate(self._get_max_pages()):

            if self.stop_parse > 10:
                break

            if i:
                self.page = page
                self._get_main_page()

            self.parse_pages()

    def parse_pages(self):
        for article_url in self._get_list_article():

            page_article = Requester(article_url)

            stop_date, date_article = self._stop_date_article(page_article)

            if stop_date:
                break

            id_in_site = self._get_id_article(page_article)

            if Collections.objects.filter(id_donor__exact=id_in_site).exists():
                continue

            id_article = article_url.split('.')[-2].split('-')[-1]

            price, currency = self._get_price(page_article)

            phones = self._get_phone(page_article, id_article)
            dict_phones = {key:value for key, value in enumerate(phones)}

            name = self._get_name(page_article)

            description = self._get_description(page_article)

            title = self._get_title(page_article),

            city = self._get_location(page_article)

            Collections.objects.create(
                create_at=date_article,
                donor=Donor.OLX,
                id_donor=id_in_site,
                city=city,
                title=title,
                description=description,
                link=article_url,
                price=price,
                currency=currency,
                phones=dict_phones,
                name=name
            )

            message = self.get_message(kwargs={
                'phones': phones,
                'name': name,
                'price': price,
                'title': title,
                'city': city,
                'description': description,
                'article_url': article_url,
                'date_article': date_article,
                'currency': currency
            })
            if self.emails_admin:
                send_mail(
                    subject='From Analyzer ads.topvykup.com.ua',
                    message=message,
                    from_email='analyzer@ads.topvykup.com.ua',
                    recipient_list=self.emails_admin,
                    fail_silently=False,
                    html_message=message
                )

    @staticmethod
    def get_message(kwargs):
        return render_to_string('message.html', kwargs)

    def _get_name(self, article):
        name = ''.join(article.get_text(self.NAME))
        if name:
            return name.replace('\n', '').strip(' ')
        else:
            return ''

    def _get_price(self, article):
        price_and_cur = ''.join(article.get_text(self.PRICE))
        p = re.compile(r'\d+')
        price = ''.join(re.findall(p, price_and_cur))
        p2 = re.compile(r'\W+')
        currency = ''.join(re.findall(p2, price_and_cur)).strip(' ')
        if currency != '$':
            currency = 'грн'
        if price:
            return price, currency
        else:
            return ''

    def _get_description(self, article):
        description = ''.join(article.get_text(self.DESCRIPTION))
        if description:
            return description.replace('\n', '').strip(' ')
        else:
            return ''

    def _get_title(self, article):
        title = ''.join(article.get_text(self.TITLE))
        if title:
            return title.replace('\n', '').strip(' ')
        else:
            return ''

    def _get_location(self, article):
        location = ''.join(article.get_text(self.LOCATION))
        if location:
            return location
        else:
            return ''

    def _get_id_article(self, article):
        id = ''.join(article.get_text(self.ID))
        p = re.compile(r'\d{9}')
        id = re.findall(p, id)
        if id:
            return id[0]
        else:
            return ''

    def _get_list_article(self):
        return self.main_page.get_link(
            self.SELECTOR_GETLINK_ARTICLES)

    def _get_main_page(self):
        self.main_page = Requester(''.join(
            [self.main_link, '?page=', self.page]))
        return self.main_page

    def _get_max_pages(self):
        data =  self._get_main_page().get_text(
            '//div[@class="pager rel clr"]//text()')
        return [i for i in data if i.isdigit()]

    def _stop_date_article(self, article):
        date_article = self._get_date_article(article)
        if date_article <= make_naive(self.stop_day):
            self.stop_parse =+ 1
        if self.stop_parse > 10:
            return True, date_article
        return False, date_article

    def _get_date_article(self, page_article):
        date_article = ' '.join(page_article.get_text(self.SELECTOR_DATE))
        p = re.compile(r'(?P<time_art>\d{2}[:]\d{2})')
        time_art = re.search(p, date_article)
        time_art = time_art.group().split(':')
        p = re.compile('(?P<date_art>\d{1,2}\s\w+\s\d{4})')
        date_art = re.search(p, date_article)
        date_art = date_art.group().split(' ')
        date_art.reverse()
        date_art[1] = mutable_month(date_art[1])
        datetime_article = datetime.datetime(
            int(date_art[0]),
            int(date_art[1]),
            int(date_art[2]),
            hour=int(time_art[0]),
            minute=int(time_art[1])
        )
        return datetime_article

    def _get_phone(self, page_article, id_article):
        phone_token = self._get_phone_token(page_article)
        if not phone_token:
            return None

        path = ''.join((self.SITE_URL, self.AJAX_PHONE,
                        id_article[2:], '/?pt=', phone_token))

        if hasattr(page_article, 'PHPSESSID'):
            phone = Requester(path, ssid=page_article.PHPSESSID).get_text()
            phone = ''.join(phone)
            try:
                phone = json.loads(phone)
                return mutable_phone(phone['value'])
            except ValueError:
                return []

    def _get_phone_token(self, page_article):
        page_article = page_article.get_text(
            '//script[contains(., "phoneToken")]/text()')
        if page_article:
            page_article = [x for x in page_article[0].split('\'')
                            if '\n' not in x]
            if page_article:
                return page_article[0]
        return False


def mutable_month(month):
    month = month.lower()
    months = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }
    return months.get(month, '01')

def mutable_phone(phone):
    p = re.compile(r'\d{7,10}')
    phone = phone.replace('-', '')
    phone = phone.replace('(', '')
    phone = phone.replace(')', '')
    phone = phone.replace('+38', '')
    phone = phone.replace('+8', '')
    phone = phone.replace(' ', '')
    if len(phone) == 12:
        if phone[0:3] == '380':
            phone = phone[2:]
    phone = re.findall(p, phone)
    return phone


# parser = ParserOlx()
# parser.run()