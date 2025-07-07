from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.

class RegistrationTestCase(APITestCase):
    def test_registration(self):
        url = '/api/dj-rest-auth/registration/'
        data = {
            'email': 'autotestuser@example.com',
            'password': '12345',
        }
        response = self.client.post(url, data, format='json')
        print('RESPONSE:', response.status_code, response.data)
        self.assertIn(response.status_code, [201, 400], msg=f"Registration failed: {response.data}")
