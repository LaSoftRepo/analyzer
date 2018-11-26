import datetime
from urllib.parse import urljoin, urlsplit
import uuid
from django.utils import timezone

import re
import requests
from django.utils.timezone import make_naive
from lxml import html
import pytesseract
from PIL import Image

from collection.models import Collections, Donor
from core import mixins
from core.utils import validate_sms_phone
from settings_analyzer.models import Settings
from settings_analyzer.validators import filter_parse
from sms_sender.sender import SmsSender

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


class ConfigParserIcar:
    parameters = {
        'new[]': 0,
        'm[]': 0,
        'n[]': 0,
        'x[]': 0,
        'y1': 1991,
        'y2': '',
        'p1': 1000,
        'p2': 5000,
        'o[]': 0,
        'c[]': 0,
        'ru': '',
        'm1': '',
        'm2': '',
        'k[]': '',
        'co[]': '',
        'd': '',
        'p': '',
        'pr': '',
        'dtp[]': 1,
        'da': 0,
        'cr[]': 0,
        'cl[]': 0,
        'ch[]': 0,
        'z[]': 0,
        'onp': 30
    }

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/41.0.2228.0 Safari/537.36'}

    @property
    def main_link(self):
        return 'http://avtobazar.infocar.ua/search-car/'


class Requester(ConfigParserIcar):
    def __init__(self, link=None, stream=False):
        if not link:
            link = self.main_link

        year_from = Settings.get_solo().date_from or '1990'
        if isinstance(year_from, datetime.date):
            year_from = year_from.year
        year_to = Settings.get_solo().date_to or ''
        if isinstance(year_to, datetime.date):
            year_to = year_to.year
        self.parameters['y1'] = year_from
        self.parameters['y2'] = year_to

        self.response = requests.get(link, params=self.parameters,
                                     headers=self.headers, stream=stream)

        self.parsed_body = html.fromstring(self.response.text)

        # html_str = html.tostring(self.response.text)
        # with open('asas.html', 'w') as f:
        #     f.write(self.response.text)

    def get_link(self, selector):
        list_link = self.parsed_body.xpath(selector)
        list_link = \
            [urljoin(self.response.url, url) for url in list_link]
        return list_link

    def get_text(self, selector='//text()'):
        return self.parsed_body.xpath(selector)


class ParserIcar(mixins.EmailSenderMixin):
    def start(self):
        print('Start Parse ICAR')
        sms = SmsSender()
        sms_enable = Settings.get_solo().enable_disable_sms
        email_enable = Settings.get_solo().enable_disable_email
        list_link = Requester().get_link(
            '//div[@class="car"]/div[@class="h"]/a/@href')
        for link_article in list_link:
            page = Requester(link=link_article)

            id_article = self._get_id_article(page)
            if not id_article:
                continue

            if Collections.objects.filter(
                    id_donor__exact=id_article).exists():
                continue

            date_article = self._get_date_article(page)
            if not date_article:
                continue

            title = self._get_title(page)

            price, currency = self._get_price(page)

            name, phones = self._get_phone(page)
            dict_phones = {key: value for key, value in enumerate(phones)}

            description = self._get_description(page)

            city = self._get_location(page)

            if not filter_parse(title, description, price, currency, city):
                continue

            collection = Collections.objects.create(
                create_at=date_article,
                donor=Donor.ICAR,
                id_donor=id_article,
                city=city,
                title=title,
                description=description,
                link=link_article,
                price=price,
                currency=currency,
                phones=dict_phones,
                name=name,
                never_send=False
            )

            if collection.sms_is_send:
                continue

            if not email_enable:
                self.send_email_to_admin(collection)

            if sms_enable:
                collection.never_send = False
                collection.save()
                sms_status = sms.send(validate_sms_phone(collection))

                if sms_status:
                    collection.sms_is_send = True
                    collection.save()
                    if email_enable:
                        self.send_email_to_admin(collection)

    def _get_location(self, page):
        data = page.get_text('//div[@id="where"]/a')
        if len(data) == 3:
            data = data[0].text + ', ' + data[1].text
        elif len(data) and len(data) <= 2:
            data = data[0].text
        return data

    def _get_description(self, page):
        data = page.get_text('//p[@id="text"]//text()')
        return ''.join(data)

    def _get_phone(self, page):
        name = page.get_text('//div[@id="author"]/strong//text()')
        if not len(name):
            name = page.get_text('//div[@id="author"]/strong/a//text()')

        phone_links = page.get_link('//div[@id="author"]/img/@src')
        phones = []
        for phone_link in phone_links:
            path = '/tmp/phone-' + str(uuid.uuid4()) + '.png'
            img = self.requests_image(phone_link, path)
            if img:
                phone = pytesseract.image_to_string(Image.open(path))
                if phone:
                    phone = self._normailize_phone(phone)
                    phones.append(phone)
        return ''.join(name), phones

    @staticmethod
    def _normailize_phone(phone):
        phone = phone.replace('+38', '')
        phone = phone.replace('(', '')
        phone = phone.replace(')', '')
        phone = phone.replace('-', '')
        phone = phone.replace(' ', '')
        return phone

    @staticmethod
    def requests_image(file_url, path):
        suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', ]
        file_name = urlsplit(file_url)[2].split('/')[-1]
        file_suffix = file_name.split('.')[1]
        i = requests.get(file_url)
        if file_suffix in suffix_list and i.status_code == requests.codes.ok:
            with open(path, 'wb') as file:
                file.write(i.content)
            return path
        else:

            return False

    def _get_price(self, page):
        data = page.get_text('//div[@id="info"]/div[@id="price"]/abbr[@id="priceabbr"]//text()')
        data = ''.join(data)
        if data and 'у.е.' in data:
            data = data.replace(' у.е.', '').replace('.', '')
            if data.isdecimal():
                data = int(data)
        return data, '$'

    def _get_title(self, page):
        data = page.get_text('//div[@id="info"]/h1//text()')
        return ''.join(data).strip(' ')

    def _get_date_article(self, page):
        data = page.get_text('//div[@id="info"]/table')
        result = False
        regex = r"(?P<date>\d{2}.\d{2}.\d{4})"
        if len(data) == 2:
            data = data[0].getchildren()
            if len(data) == 5:
                matches = list(re.finditer(regex, data[3].text))
                if matches:
                    result = datetime.datetime.strptime(
                        matches[0].groupdict().get('date'),
                        '%d.%m.%Y')
        if isinstance(result, datetime.datetime):
            try:
                if result < make_naive(self.stop_day):
                    raise ValueError
            except ValueError:
                result = False
        return result

    def _get_id_article(self, page):
        data = page.get_text('//div[@id="info"]/table')
        result = False
        if len(data) == 2:
            data = data[0].getchildren()
            if len(data) == 5:
                data = data[2].getchildren()
                if len(data) == 2:
                    result = data[1].text.split(' ')[1].strip(' ')
        return result

    @property
    def stop_day(self):
        return timezone.now() - datetime.timedelta(days=7)


# if __name__ == '__main__':
#     p = ParserIcar()
#     p.start()
