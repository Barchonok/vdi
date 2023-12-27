from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
url = 'http://127.0.0.1:8000/api/v1/'
class AdminTests(APITestCase):

    def test_login(self):

        data = {
            'login': 'admin',
            'password': 'admin',
        }
        response = self.client.post(url+ 'api-token-login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)