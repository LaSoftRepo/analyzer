from django.db import models
from django.contrib.postgres.fields import JSONField


class Donor:
    OLX = 'olx'
    AUTORIA = 'auto.ria'
    RST = 'rst.ua'
    ICAR = 'avtobazar.infocar.ua'
    SITE = (
        (OLX, 'olx'),
        (AUTORIA, 'auto.ria'),
        (RST, 'rst.ua'),
        (ICAR, 'avtobazar.infocar.ua')
    )


class Collections(models.Model):
    create_at = models.DateTimeField(
        auto_created=True,
        verbose_name='Create date/time'
    )
    never_send = models.BooleanField(default=True)
    donor = models.CharField(
        max_length=50,
        verbose_name='Site donor',
        choices=Donor.SITE
    )
    id_donor = models.CharField(
        verbose_name='ID',
        blank=True,
        max_length=100
    )
    city = models.CharField(
        max_length=100,
        verbose_name='City',
        blank=True
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Title',
        blank=True
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True
    )
    link = models.URLField(
        verbose_name='Link',
        blank=True
    )
    price = models.IntegerField(
        verbose_name='Price',
        blank=True
    )
    currency = models.CharField(
        verbose_name='Carrency',
        blank=True,
        max_length=20
    )
    phones = JSONField(
        null=True
    )
    name = models.CharField(
        verbose_name='Name',
        max_length=100,
        blank=True
    )
    sms_is_send = models.BooleanField(
        verbose_name='SMS',
        default=False
    )
    email_is_send = models.BooleanField(
        verbose_name='Email is send',
        default=False
    )

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    def __str__(self):
        return f'{self.id_donor} => {self.link}'
