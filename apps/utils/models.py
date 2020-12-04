from django.db import models
from django.utils.translation import ugettext as _


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, editable=False, verbose_name=_('Дата создания'), null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Время создания'), null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Время обновления'), null=True)
    created_by = models.ForeignKey('authentication.User', models.SET_NULL, null=True, blank=True,
                                   related_name='created_%(class)ss', verbose_name=_('Создано пользоветем'))
    updated_by = models.ForeignKey('authentication.User', models.SET_NULL, null=True, blank=True,
                                   related_name='updated_%(class)ss', verbose_name=_('Обновлено пользоветем'))

    class Meta:
        abstract = True
