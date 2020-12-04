from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone(value):
    if type(value) != str or not value.startswith('998') or len(value) != 12:
        raise ValidationError(
            _('%(value)s не является корректным номером телефона'),
            params={'value': value},
        )
