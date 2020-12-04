from django.urls import reverse
from rest_framework.test import APITestCase


PASS = '12345'
ERR_PASS = '123'


class AuthenticationTest(APITestCase):
    fixtures = ['user', 'token']

    def test_login(self):
        response = self.client.post(
            reverse('authentication:login'),
            {'username': 'simple_user', 'password': ERR_PASS}
        )
        self.assertEqual(response.data['password'], 'Неверный пароль')
        self.assertEqual(401, response.status_code, response.data)

        response = self.client.post(
            reverse('authentication:login'),
            {'username': 'simple_user1', 'password': ERR_PASS}
        )
        self.assertEqual(response.data['username'], 'Пользователь не существует')
        self.assertEqual(401, response.status_code, response.data)

        response = self.client.post(
            reverse('authentication:login'),
            {'username': 'simple_user', 'password': PASS}
        )
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(200, response.status_code, response.data)

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token bd8eab5971cdfea2c25763752dbc4f15c98ad9e2')
        url = reverse('authentication:change_password')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(url, {'password': ERR_PASS, 'new_password': ERR_PASS})
        self.assertEqual(response.data['password'], 'Неверный пароль')
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(url, {'password': PASS, 'new_password': PASS})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)

    def test_tokens(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token asuwhhwhwhehhedhdhddsjhfgsdf')
        url = reverse('authentication:change_password')
        response = self.client.post(url)
        self.assertEqual(response.data['detail'], 'Недопустимый токен.')
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token bd8eab5971cdfea2c25763752dbc4f15c98ad9e3')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Пользователь неактивен или удален.')
