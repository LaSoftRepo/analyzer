from zeep import Client

from django.core.mail import send_mail

from collection.models import Collections
from users.models import User


class SmsSender:
    text = 'Готовы выкупить ваше авто, 90% рыночной стоимости, ' \
           'деньги в день обращения. 000-111-22-33'

    def __init__(self):
        self.error_message = ''
        self.msg_status = ''
        self.client = Client('http://turbosms.in.ua/api/wsdl.html')
        self.auth = self.client.service.Auth(login='analyzer',
                                             password='analyzer99')
        self.balance = self.get_balance()

    def send(self, phone):
        if self.auth == 'Вы успешно авторизировались':
            if float(self.balance):
                self._result(phone)
            else:
                self.error_message = f'Ваш баланс {self.balance}'
        elif self.auth == 'Неверный логин или пароль':
            self.error_message = 'Неверный логин или пароль'

    def _result(self, phone):
        result = self.client.service.SendSMS(sender='Top Vykup',
                                             destination=phone,
                                             text=self.text)
        if result[0] == 'Сообщения успешно отправлены':
            self.msg_status = self.get_msg_status(result[1])
        else:
            self.error_message = result[0]

    def get_msg_status(self, sms_id):
        self.msg_status = self.client.service.GetMessageStatus(
            MessageId=sms_id)
        return self.msg_status

    def get_balance(self):
        return self.client.service.GetCreditBalance()


class ClientSmsSender:
    def __init__(self):
        self.get_articles = Collections.objects.filter(sms_is_send=False)
        self.sms = SmsSender()

    def start(self):
        for article in self.get_articles:
            phone = self._get_phone(article)
            if phone:
                self.sms.send(phone)
                if self.sms.msg_status == 'Отправлено':
                    article.sms_is_send = True
                    self.send_mails(phone)
                else:
                    article.phones['error'] = self.sms.error_message
                article.save()
                # print(self.sms.msg_status)
                # print(self.sms.error_message)
                # print(self.sms.balance)

    def _get_phone(self, article):
        for k, phone in article.phones.items():
            phone = self._normalize_phone(phone)
            if phone:
                return phone
            else:
                article.phones['error'] = 'ERROR PHONE'
                article.save()
                break

    @staticmethod
    def _normalize_phone(phone):
        if len(phone) == 10:
            return ''.join(('+38', phone))
