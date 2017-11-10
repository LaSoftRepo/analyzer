import datetime
from urllib.parse import urljoin
from django.utils import timezone

import requests
from django.utils.timezone import make_naive
from lxml import html

from collection.models import Collections, Donor
from core.utils import validate_sms_phone
from settings_analyzer.validators import filter_parse
from sms_sender.sender import SmsSender
from core import mixins


class ConfigParserRst:

    parameter = {
        'task': 'newresults',
        'make[]': 0,
        'year[]': [1991, 2017],
        'price[]': [1000, 5000],
        'engine[]': [0, 0],
        'gear': 0,
        'fuel': 0,
        'drive': 0,
        'condition': '3,4',
        'from': 'sform',
        'start': '2'
    }

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/41.0.2228.0 Safari/537.36'}

    @property
    def main_link(self):
        return 'http://rst.ua/oldcars/'


class Requester(ConfigParserRst):
    def __init__(self, page=1, link=None):
        self.parameter['start'] = page
        if not link:
            self.link = self.main_link
        else:
            self.link = link
            self.parameter = {}
        self.response = requests.get(self.link, params=self.parameter, headers=self.headers)
        # print(self.response.content)
        self.parsed_body = html.fromstring(self.response.text)
        # html_str = html.tostring(self.response.text)
        # with open('asas.html', 'w') as f:
        #     f.write(self.response.text)

    def get_link(self, selector):
        list_link = self.parsed_body.xpath(selector)
        list_link = \
            [urljoin(self.response.url, url)for url in list_link]
        return list_link

    def get_text(self, selector='//text()'):
        return self.parsed_body.xpath(selector)


class ParserRst(mixins.EmailSenderMixin):

    def start(self):
        sms = SmsSender()
        for i in range(1, 8):
            list_link_articles = Requester(i).get_link('//a[@class="rst-ocb-i-a"]/@href')
            for article_link in list_link_articles:
                page_article = Requester(link=article_link)

                id_article = self._get_id_article(page_article)

                if Collections.objects.filter(
                        id_donor__exact=id_article).exists():
                    continue

                date_article = self._get_date_article(page_article)
                if not date_article:
                    continue

                title = self._get_title(page_article)

                price, currency = self._get_price(page_article)

                name, phones = self._get_phone(page_article)
                dict_phones = {key: value for key, value in enumerate(phones)}

                description = self._get_description(page_article)

                city = self._get_location(page_article)

                if 'отсутствуют' in name:
                    continue

                if not filter_parse(title, description, price, currency, city):
                    continue

                collection = Collections.objects.create(
                    create_at=date_article,
                    donor=Donor.RST,
                    id_donor=id_article,
                    city=city,
                    title=title,
                    description=description,
                    link=article_link,
                    price=price,
                    currency=currency,
                    phones=dict_phones,
                    name=name
                )

                if collection.sms_is_send:
                    continue

                sms_status = sms.send(validate_sms_phone(collection))

                if sms_status:
                    collection.sms_is_send = True
                    collection.save()
                    self.send_email_to_admin(collection)

    @property
    def stop_day(self):
        return timezone.now() - datetime.timedelta(days=7)

    def _get_date_article(self, page_article):
        datetime_object = ''
        result = page_article.get_text(
            '//div[@class="rst-page-oldcars-item-option-block rst-uix-clear"]/table[@class="rst-uix-table-superline"]/tr[@class="rst-uix-grey"]/td/span[@class="rst-uix-black"]/text()')
        if not result:
            result = page_article.get_text(
                '//ul[@class="rst-uix-list-superline"]/li[@class="rst-uix-grey"]/span/span[@class="rst-uix-black"]/text()')
        if result:
            result = ''.join(result)
            datetime_object = datetime.datetime.strptime(result,
                                            '%d.%m.%Y')

        if not datetime_object:
            return False

        if datetime_object < make_naive(self.stop_day):
            return False

        return datetime_object

    def _get_location(self, page_article):
        result = page_article.get_text('//ul[@class="rst-uix-list-superline"]/li/span/span[@class="rst-uix-grey"]/a/text()')
        if not result:
            result = page_article.get_text('//div[@class="rst-page-oldcars-item-option-block rst-uix-clear"]/table[@class="rst-uix-table-superline"]/tr/td/span[@class="rst-uix-grey"]//text()')
        result = ''.join(result)
        result = result.split('-')[-1]
        result = result.replace('\r\n', '').replace(')', '').strip(' ')
        if 'пробег' in result:
            return ''
        return result

    def _get_description(self, page_article):
        result = page_article.get_text('//div[@id="rst-page-oldcars-item-option-block-container-desc"]/text()')
        result = ''.join(result)
        result = result.replace('\r\n', '').strip(' ')
        return result

    def _get_title(self, page_article):
        result = page_article.get_text('//h2[@id="rst-page-oldcars-item-header"]/text()')
        return ''.join(result)

    def _get_id_article(self, page_article):
        result = page_article.get_text('//div[@id="rst-page-oldcars-item-id"]/p/strong/text()')
        return ''.join(result)

    def _get_price(self, page_article):
        result = page_article.get_text('//span[@class="rst-uix-price-param"]/strong/text()')
        result = ''.join(result)
        if '\'' in result:
            result = result.replace('\'', '')
        result = result.replace('грн', '')
        result = result.strip(' ')

        # if result.isdigit():
        #     result = int(result)
        # else:
        #     return 0

        return result, 'грн'

    def _get_phone(self, page_article):
        name = ''
        phones = []
        result = page_article.get_text('//div[@class="rst-oc-item-option-block"]/div/text()')
        if not result:
            result = page_article.get_text('//p[@class="rst-page-oldcars-item-option-block-container"]//text()')
            if not result:
                result = page_article.get_text('//div[@class="rst-page-oldcars-item-option-block-container"]//text()')
        copy_result = []

        for resul in result:
            copy_result.append(resul.replace('тел.: ', '').replace('\xa0', ''))
        clean_result = [x for x in copy_result if x]

        if clean_result and not clean_result[0].isdigit():
            name = clean_result[0]

        new_phone = ''
        for item in clean_result:
            if item.isdigit():
                if len(item) <= 4:
                    new_phone += item
                elif item[0] == '0':
                    phones.append(item)
        if new_phone:
            phones.append(new_phone)
        # print(clean_result)
        return name, phones

    def _normalaze_phone(numb):
        pass





if __name__ == '__main__':
    start = ParserRst()
    start.start()
