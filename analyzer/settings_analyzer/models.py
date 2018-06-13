from django.db import models
from solo.models import SingletonModel


class Settings(SingletonModel):
    price_usd_from = models.IntegerField(blank=True, null=True)
    price_usd_to = models.IntegerField(blank=True, null=True)
    price_hrn_from = models.IntegerField(blank=True, null=True)
    price_hrn_to = models.IntegerField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    message_text = models.TextField(blank=True, null=True)
    enable_disable_email = models.BooleanField(default=False)
    enable_disable_sms = models.BooleanField(default=False)


class StatusSiteParse(models.Model):
    name = models.CharField(
        max_length=50
    )
    is_enable = models.BooleanField(default=True)


class StopWordList(models.Model):
    word = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='слово'
    )

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Stop Word'