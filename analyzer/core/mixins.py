from django.core.mail import send_mail
from django.template.loader import render_to_string

from users.models import User


class EmailSenderMixin:
    def __init__(self):
        self.emails_admin = User.objects.filter(
            is_get_email=True).values_list('email', flat=True)

    def send_email_to_admin(self, article):
        message = self.get_message(kwargs={
            'phones': self._get_mixin_phones(article.phones),
            'name': article.name,
            'price': article.price,
            'title': article.title,
            'city': article.city,
            'description': article.description,
            'article_url': article.link,
            'date_article': article.create_at,
            'currency': article.currency
        })
        if self.emails_admin:
            status = send_mail(
                subject='Новая заявка — ads.topvykup.com.ua',
                message=message,
                from_email='analyzer@ads.topvykup.com.ua',
                recipient_list=self.emails_admin,
                fail_silently=False,
                html_message=message
            )
            if status:
                article.email_is_send = True
                article.save()

    @staticmethod
    def _get_mixin_phones(phones):
        phones_list = []
        for k, phone in phones.items():
            phones_list.append(phone)
        return phones_list

    @staticmethod
    def get_message(kwargs):
        return render_to_string('message.html', kwargs)