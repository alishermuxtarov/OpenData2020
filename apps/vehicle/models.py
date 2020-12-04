from django.db import models
from django.utils.translation import ugettext as _

from utils.models import BaseModel


class AdSource(models.TextChoices):
    OLX = 'olx', _('olx.uz')
    AVTOELON = 'avtoelon', _('avtoelon.uz')


class TransmissionType(models.TextChoices):
    AUTOMATIC = 'automatic', _('Автоматическая')
    MANUAL = 'manual', _('Механическая')
    OTHER = 'other', _('Другое')


class VehicleCondition(models.TextChoices):
    PERFECT = 'perfect', _('Отличное')
    GOOD = 'good', _('Хорошее')
    MEDIOCRE = 'mediocre', _('Среднее')
    NEEDS_REPAIRS = 'needs_repairs', _('Требует ремонта')


class Brand(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'vehicle_brands'
        verbose_name = _("Производитель")
        verbose_name_plural = _("Производители")


class Model(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'vehicle_models'
        verbose_name = _("Модель машины")
        verbose_name_plural = _("Модели машин")


class BodyType(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'vehicle_body_types'
        verbose_name = _("Тип кузова")
        verbose_name_plural = _("Типы кузова")


class BodyColor(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'vehicle_body_colors'
        verbose_name = _("Цвет кузова")
        verbose_name_plural = _("Цвета кузова")


class FuelType(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'vehicle_fuel_types'
        verbose_name = _("Вид топлива")
        verbose_name_plural = _("Виды топлива")


class AdditionalOption(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'vehicle_additional_options'
        verbose_name = _("Дополнительная опция")
        verbose_name_plural = _("Дополнительные опции")


class VehicleAd(BaseModel):
    source = models.CharField(_('Источник объявления'), max_length=20, choices=AdSource.choices)
    title = models.TextField(_('Заголовок объяления'))
    description = models.TextField(_('Заголовок объяления'))
    url = models.URLField(_('URL объявления'))
    manufactured_year = models.SmallIntegerField(_('Год выпуска'))
    number_of_owners = models.SmallIntegerField(_('Количество хозяев'))
    transmission_type = models.CharField(_('Трансмиссия'), max_length=20, choices=TransmissionType.choices)
    condition = models.CharField(_('Состояние'), max_length=20, choices=VehicleCondition.choices)
    engine_capacity = models.SmallIntegerField(_('Объем двигателя (sm3)'))
    driven_km = models.SmallIntegerField(_('Пробег (км)'))
    price_usd = models.BigIntegerField(_('Цена USD'))
    price_uzs = models.BigIntegerField(_('Цена UZS'))

    brand = models.ForeignKey(Brand, models.CASCADE, verbose_name=_('Производитель'))
    model = models.ForeignKey(Model, models.CASCADE, verbose_name=_('Модель'))
    body_type = models.ForeignKey(BodyType, models.CASCADE, verbose_name=_('Тип кузова'))
    body_color = models.ForeignKey(BodyColor, models.CASCADE, verbose_name=_('Цвет кузова'))
    fuel_types = models.ManyToManyField(FuelType, 'ads', verbose_name=_('Виды топлива'))
    additional_options = models.ManyToManyField(AdditionalOption, 'ads', verbose_name=_('Дополнительные опции'))

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'vehicle_ads'
        verbose_name = _("Объявление о продаже машины")
        verbose_name_plural = _("Объявления о продаже машин")
