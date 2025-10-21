from http import HTTPStatus
from django.test import TestCase, Client
from user.models import User
from ninja_jwt.controller import NinjaJWTDefaultController


def get_user_login_payload():
    payload = {
        "email": "crystal@gems.com",
        "password": "WatermelonSteven12"
    }
    return payload


def createUser():
    payload = {
        "firstName": "Steven",
        "lastName": "Universe",
        "email": "crystal@gems.com",
        "password": "WatermelonSteven12"
    }

    user = User(**payload)
    user.set_password(user.password)
    user.save()

class UserAuthTest(TestCase):
    def setUp(self):
        self.client = Client(NinjaJWTDefaultController)

    # Testing that a newly created user is able to access ninja-jwt endpoints:
    # token/pair, token/refresh, token/verify
    def test_auth(self):
        createUser()

        res = self.client.post('/api/token/pair', data=get_user_login_payload(), content_type="application/json")

        TestCase.assertEqual(self, res.status_code, HTTPStatus.OK, res.content)

        refresh_token = res.json().get('refresh')
        access_token = res.json().get('access_token')

        print(refresh_token)



