from django.utils.translation import ugettext as _

from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import serializers

from utils.serializers import ValidatorSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_permissions(user):
        return user.get_all_permissions()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'permissions')


class LoginValidator(ValidatorSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, data):
        user = User.objects.filter(username=data.get('username')).first()

        if user:
            if not user.is_active:
                raise ValidationError({'username': _("Пользователь не активен")})

            if not user.check_password(data.get('password')):
                raise AuthenticationFailed({'password': _("Неверный пароль")})

            return data, user
        else:
            raise AuthenticationFailed({'username': _("Пользователь не существует")})


class LoginDataSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()
    data = serializers.SerializerMethodField(read_only=True, allow_null=True)

    @staticmethod
    def get_data(data):
        return UserSerializer(data.get('user')).data


class ChangePasswordSerializer(ValidatorSerializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
