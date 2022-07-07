import pytest
import json
from django.db import IntegrityError
from django.test import TestCase
from users.models import User


# Create your tests here.
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "22343454565",
            "phone_number": "+256702607610",
            "user_type": "Admin"
        }
        user = User.objects.create("test@gmail.com", "password", **extra_fields)
        return super().setUpTestData()

    def test_create_user_model(self):
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454555",
            "phone_number": "+256782607600",
            "user_type": "Admin"
        }
        user = User.objects.create("basp18@gmail.com", "password", **extra_fields)
        self.assertEqual(user.email, 'basp18@gmail.com')
        self.assertEqual(user.phone_number, extra_fields['phone_number'])
        self.assertEqual(user.nin, extra_fields['nin'])
        self.assertEqual(user.user_type, extra_fields['user_type'])
        self.assertEqual(user.is_superuser, False)

    def test_create_super_user_model(self):
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454555",
            "phone_number": "+256782607600",
            "user_type": "Admin",
        }
        user = User.objects.create_superuser("basp18@gmail.com", "password", **extra_fields)
        self.assertEqual(user.email, 'basp18@gmail.com')
        self.assertEqual(user.phone_number, extra_fields['phone_number'])
        self.assertEqual(user.nin, extra_fields['nin'])
        self.assertEqual(user.user_type, extra_fields['user_type'])
        self.assertEqual(user.is_superuser, True)

    def test_create_user_fails_with_non_unique_email(self):
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454555",
            "phone_number": "+256782607600",
            "user_type": "Admin"
        }
        with pytest.raises(IntegrityError):
            user = User.objects.create("test@gmail.com", "password", **extra_fields)

    def test_create_user_fails_with_missing_fields(self):
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "22343454565",
            "phone_number": "+256782607600",
            "user_type": "Admin"
        }
        with pytest.raises(ValueError, match="The email must be given") as excinfo:
            user = User.objects.create("", "password", **extra_fields)

class UserLoginTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "22343454565",
            "phone_number": "+256702607610",
            "user_type": "Admin"
        }
        user = User.objects.create("test@gmail.com", "password", **extra_fields)

    def test_user_login(self):
        response = self.client.login(email='test@gmail.com', password='password')
        user = User.objects.filter(email='test@gmail.com').first()
        self.assertEqual(response, True)
        self.assertEqual(self.client.session['_auth_user_id'], str(user.id))

    def test_user_login_fails(self):
        response = self.client.login(email='test@gmail.com', password='welcome')
        self.assertEqual(response, False)

    def test_user_login_json(self):
        response = self.client.post(
            '/token/',
            {
                "email": 'test@gmail.com',
                "password" : "password"
            }
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertIn('refresh', dict_res.keys())
        self.assertIn('access', dict_res.keys())

    def test_user_login_fails_with_wrong_credentials(self):
        response = self.client.post(
            '/token/',
            {
                "email": 'test@gmail.com',
                "password" : "welcome"
            }
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertDictEqual(dict_res, {'detail': 'No active account found with the given credentials'})

    def test_user_login_fails_with_mising_password_field(self):
        response = self.client.post(
            '/token/',
            {
                "email": 'test@gmail.com',
            }
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertDictEqual(dict_res, {'password': ['This field is required.']})

    def test_user_login_fails_with_mising_email_field(self):
        response = self.client.post(
            '/token/',
            {
                "password" : "welcome"
            }
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertDictEqual(dict_res, {'email': ['This field is required.']})

class UserListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "22343454565",
            "phone_number": "+256702607610",
            "user_type": "Admin"
        }
        user = User.objects.create("test@gmail.com", "password", **extra_fields)
        extra_fields2 = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454665",
            "phone_number": "+256782707610",
            "user_type": "Worker"
        }
        user = User.objects.create("normol_user@gmail.com", "password", **extra_fields2)

    def test_get_all_users(self):
        response = self.client.get('/user/')
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(len(dict_res), 6)
        for user in dict_res:
            if user['email'] == 'test@gmail.com':
                self.assertDictEqual(user, {
                    "nin":"22343454565",
                    "phone_number":"+256702607610",
                    "email":"test@gmail.com",
                    "first_name":"Phiona",
                    "last_name":"Basemera",
                    "user_type":"Admin"
                    })
