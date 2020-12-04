from django.utils.translation import ugettext as _
from django.utils import timezone

from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginValidator, LoginDataSerializer, ChangePasswordSerializer
from .models import Token, User


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginValidator

    def post(self, request):
        _, user = self.serializer_class.check(request.data)
        token, _ = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return Response(LoginDataSerializer(instance={'token': token.key, 'user': user}).data)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("password")):
                return Response({"password": _("Неверный пароль")}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
