from http import HTTPStatus
from django.test import TestCase, Client
from ninja.testing import TestClient

from user.models import User
from ninja_jwt.controller import NinjaJWTDefaultController


def get_user_login_payload():
    payload = {
        "email": "crystal@gems.com",
        "password": "WatermelonSteven12"
    }
    return payload

class UserApiTest(TestCase):
    def setUp(self):
        self.client = TestClient(NinjaJWTDefaultController)

    def createUser(self):
        payload = {
            "firstName": "Steven",
            "lastName": "Universe",
            "email": "crystal@gems.com",
            "password": "WatermelonSteven12"
        }

        self.client.post('user', json=payload, content_type="application/json")

    # Testing that a newly created user is able to access ninja-jwt endpoints:
    # token/pair, token/refresh, token/verify
    def test_auth(self):
        self.createUser()

        res = self.client.post('/api/token/pair', json=get_user_login_payload(), content_type="application/json")

        TestCase.assertEqual(self, res.status_code, HTTPStatus.OK, res)


