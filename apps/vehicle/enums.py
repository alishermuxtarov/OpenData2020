from django.db import models
from django.utils.translation import ugettext as _


class AdSource(models.TextChoices):
    OLX = 'olx', _('olx.uz')
    AVTOELON = 'avtoelon', _('avtoelon.uz')


class TransmissionType(models.TextChoices):
    AUTOMATIC = 'automatic', _('Автоматическая')
    MANUAL = 'manual', _('Механическая')
    OTHER = 'other', _('Другая')


class VehicleCondition(models.TextChoices):
    PERFECT = 'perfect', _('Отличное')
    GOOD = 'good', _('Хорошее')
    MEDIOCRE = 'mediocre', _('Среднее')
    NEEDS_REPAIRS = 'needs_repairs', _('Требует ремонта')
