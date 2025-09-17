from http import HTTPStatus
from django.test import TestCase
from ninja.testing import TestClient

from user.models import User
from user.router import router

def get_successful_payload():
    payload = {
        "firstName": "Steven",
        "lastName": "Universe",
        "email": "crystal@gems.com",
        "password": "WatermelonSteven12"
    }
    return payload

# Missing required fields
def get_bad_formed_payload():
    payload = {
        "firstName": "Steven",
        "lastName": "Universe",
    }
    return payload

# Missing required fields
def get_empty_str_payload():
    payload = {
        "firstName": "Steven",
        "lastName": "",
        "email": "crystal@gems.com",
        "password": ""
    }
    return payload


class UserApiTest(TestCase):
    def setUp(self):
        self.client = TestClient(router)

    # Verify creation of user in db.
    def test_create_user_with_valid_data(self):
        res = self.client.post('user', json=get_successful_payload(), content_type="application/json")

        TestCase.assertEqual(self, res.status_code, HTTPStatus.OK, f'Status code should have been 200, instead was {res.status_code}')

        try:
            user = User.objects.get(email="crystal@gems.com")

            # Verify fields besides password have been correctly inserted
            TestCase.assertEqual(self, user.firstName, "Steven", "User firstName in db does not match req.firstName")
            TestCase.assertEqual(self, user.lastName, "Universe", "User lastName in db does not match req.lastName")
            TestCase.assertEqual(self, user.email, "crystal@gems.com", "User email in db does not match req.email")
        except User.DoesNotExist: assert False, 'User was not created in database'


    def test_create_user_with_invalid_data(self):
        res = self.client.post('user', json=get_bad_formed_payload(), content_type="application/json")

        TestCase.assertEqual(self, res.status_code, HTTPStatus.UNPROCESSABLE_CONTENT,f'Status code should have been 422, instead was {res.status_code}')

        res = self.client.post('user')

        TestCase.assertEqual(self, res.status_code, HTTPStatus.UNPROCESSABLE_CONTENT,f'Status code should have been 422, instead was {res.status_code}')


    def test_create_user_with_empty_str_values(self):
        res = self.client.post('user', json=get_empty_str_payload(), content_type="application/json")

        TestCase.assertEqual(self, HTTPStatus.BAD_REQUEST, res.status_code, f'Status code should have been 400, instead was {res.status_code}')


