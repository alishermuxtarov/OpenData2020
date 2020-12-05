import binascii
import os

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name=_('Последняя активность'))

    phone = models.BigIntegerField(null=True)
    telegram_id = models.BigIntegerField(_("Telegram id"), editable=False, null=True, blank=True)

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        app_label = 'authentication'


class Token(models.Model):
    key = models.CharField(max_length=40, verbose_name=_("Ключ"), unique=True)
    user = models.ForeignKey(User, models.CASCADE, related_name='tokens', verbose_name=_("Пользователь"))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name=_(u'Время создания'))

    def save(self, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        return super().save(**kwargs)

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'authentication_tokens'
        verbose_name = _("Ключ доступа")
        verbose_name_plural = _("Ключи доступа")
