from datetime import datetime, timedelta
# from urllib.parse import urljoin

import requests
from django.utils.timezone import make_naive
from lxml import html

from django.utils import timezone

from core import mixins
from collection.models import Donor, Collections
from core.utils import validate_sms_phone
from sms_sender.sender import SmsSender


class Requester(object):

    def __init__(self, link):
        self.link = link
        self.response = requests.get(self.link)

    def get_json(self):
        return self.response.json()

    def get_ids_article(self):
        return self.response.json().get('result', {}).get('search_result', {})\
            .get('ids')

    def get_text(self, selector='//text()'):
        parsed_body = html.fromstring(self.response.text)
        return parsed_body.xpath(selector)


class WrapperRiaApi:
    api_key = '0nWsipzwGqjWq5xJzn3MlGPhfK5IvI5C1NPfax5L'
    link = 'https://developers.ria.com/auto'
    link_site = 'https://auto.ria.com'

    @property
    def main_link(self):
        return f'{self.link}/search' \
               f'?api_key={self.api_key}' \
               '&category_id=1' \
               '&s_yers[0]=1990' \
               '&po_yers[0]=2017' \
               '&price_ot=1000' \
               '&price_do=5000' \
               '&currency=1' \
               '&abroad=2' \
               '&custom=1' \
               '&damage=2' \
               '&fuelRatesType=city' \
               '&marka_id=0' \
               '&model_id[0]=0' \
               '&engineVolumeFrom=' \
               '&engineVolumeTo=' \
               '&power_name=1' \
               '&countpage=100'

    def article_link(self, id_article):
        return f'{self.link}/info?api_key={self.api_key}&auto_id={id_article}'


class ParserRia(mixins.EmailSenderMixin, WrapperRiaApi):

    def start(self):
        sms = SmsSender()
        ids = Requester(self.main_link).get_ids_article()
        collections = Collections.objects.filter(
            donor=Donor.AUTORIA).values_list('id_donor', flat=True)
        for id_article in ids:
            if id_article in collections:
                continue

            data_article = Requester(self.article_link(id_article)).get_json()

            phones = [self._normailize_phone(data_article)]
            dict_phones = {key: value for key, value in enumerate(phones)}

            date_article = self._get_date_article(data_article)
            if isinstance(date_article, bool):
                continue

            city = data_article.get('locationCityName', '')

            description = data_article.get('autoData', {})\
                .get('description', '')
            title = data_article.get('title', '')

            link = ''.join([self.link_site,
                            data_article.get('linkToView', '')])
            name = self._get_name(link)

            price = data_article.get('USD', '')

            collection = Collections.objects.create(
                create_at=date_article,
                donor=Donor.AUTORIA,
                id_donor=id_article,
                city=city,
                title=title,
                description=description,
                link=link,
                price=price,
                currency='$',
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

    @staticmethod
    def _get_name(link):
        name = Requester(link).get_text(
            '//dt[@class="user-name"]//strong/text()')
        if name:
            return ''.join(name)
        return ''

    @property
    def stop_day(self):
        return timezone.now() - timedelta(days=7)

    def _get_date_article(self, data_article):
        data_article = data_article.get('addDate')
        if data_article:
            try:
                date_article = datetime.strptime(
                    data_article, '%Y-%m-%d %H:%M:%S')
                if date_article < make_naive(self.stop_day):
                    raise ValueError
                else:
                    return date_article
            except ValueError:
                return False

    @staticmethod
    def _normailize_phone(phone):
        phone = phone.get('userPhoneData', {}).get('phone')
        if phone:
            phone = phone.replace('(', '')
            phone = phone.replace(')', '')
            phone = phone.replace(' ', '')
            phone = phone.replace('-', '')
            return phone
        return ''
