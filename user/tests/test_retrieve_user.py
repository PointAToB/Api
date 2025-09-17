from http import HTTPStatus
from django.test import TestCase
from user.models import User
from user.router import router
from ninja.testing import TestClient

def getPayload():
    payload = {
        "firstName": "Steven",
        "lastName": "Universe",
        "email": "crystal@gems.com",
        "password": "WatermelonSteven12"
    }
    return payload

class UserRetrieveTest(TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def test_retrieve_user(self):
        self.user = User.objects.create(**getPayload())

        self.user.login(email=getPayload().get('email'), password=getPayload().get('password'))

        res = self.client.get('user')

        TestCase.assertEqual(self, res.status_code, HTTPStatus.OK, res)