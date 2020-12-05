from django.utils.translation import ugettext as _
from django.db import models

from utils.models import BaseModel


class Region(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')
        db_table = 'reference_regions'


class Area(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255, unique=True)
    region = models.ForeignKey(Region, models.CASCADE, 'areas', verbose_name=_('Регион'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Город/Район')
        verbose_name_plural = _('Города/Районы')
        db_table = 'reference_areas'
