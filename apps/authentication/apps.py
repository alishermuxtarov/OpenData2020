from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'authentication'
    verbose_name = _('Аутентификаия')
