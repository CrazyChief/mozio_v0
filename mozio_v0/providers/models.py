from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djmoney.models.fields import MoneyField, CurrencyField
from languages.fields import LanguageField
from phonenumber_field.modelfields import PhoneNumberField


class Provider(models.Model):
    """
    Provider's model
    """
    name = models.CharField(_('Name'), max_length=256)
    email = models.EmailField(_('Email'), unique=True)
    phone_number = PhoneNumberField()
    language = LanguageField()
    currency = CurrencyField()
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')

    def __str__(self):
        return f'{self.name} Provider'


class ServiceArea(models.Model):
    """
    Service area model (which represent areas of each Provider)
    relates to Provider model
    """
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, null=True,
        verbose_name=_('Provider'))
    polygon_name = models.CharField(
        _('Polygon name'), max_length=256, blank=True
    )
    price = MoneyField(
        max_digits=19, decimal_places=4, null=True, default_currency='USD')
    polygon = ArrayField(
        ArrayField(
            models.DecimalField(max_digits=23, decimal_places=20)
        ), verbose_name=_('Polygon')
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Service Area')
        verbose_name_plural = _('Service Areas')

    def __str__(self):
        return f'{self.polygon_name} Service Area'
