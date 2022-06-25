from django.test import TestCase
from django.db import IntegrityError
import pytest
import json
from rest_framework.test import force_authenticate
from .views import ListCreateAPIView

# Create your tests here.
from users.models import User
from .models import Department

class DepartmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454565",
            "phone_number": "+256782607610",
            "user_type": "Admin"
        }
        user = User.objects.create("admin@gmail.com", "password", **extra_fields)
        # return super().setUpTestData()

    def test_create_department_successful(self):
        user = User.objects.filter(email='admin@gmail.com').first()
        dept = Department.objects.create(name='engineering', manager=user)
        self.assertEqual(dept.name, 'engineering')
        self.assertEqual(dept.manager, user)

    def test_create_user_unsuccesful_with_missing_field(self):
        user = User.objects.filter(email='admin@gmail.com').first()
        with pytest.raises(IntegrityError, match='null value in column "name"') as excInfo:
            dept = Department.objects.create(name=None, manager=user)

class DepartmentCreateApiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454565",
            "phone_number": "+256782607610",
            "user_type": "Admin"
        }
        user = User.objects.create("admin@gmail.com", "password", **extra_fields)

        extra_fields2 = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454465",
            "phone_number": "+256772607610",
            "user_type": "Worker"
        }
        user = User.objects.create("worker@gmail.com", "password", **extra_fields2)


    def _login_user(self, email='admin@gmail.com'):
        token = self.client.post(
            '/token/',
            {
            "email":email,
            "password": "password"
        })
        res = token.content.decode('utf-8')
        dict_res = json.loads(res)
        return dict_res['access']

    def _make_decode_response(self, res):
        res = res.content.decode('utf-8')
        dict_res = json.loads(res)
        return dict_res

    def test_successfully_create_department(self):
        token = self._login_user()
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token,
            }
        response = self.client.post(
            '/department/',
            {
                "name": "sales",
	            "manager": 1
            },
            **auth_headers
        )
        dict_res = self._make_decode_response(response)
        self.assertEqual(dict_res, {"name":"sales","manager":1})

    def test_fails_when_no_credentials(self):
        response = self.client.post(
            '/department/',
            {
                "name": "sales",
	            "manager": 1
            },
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, {'detail': 'Authentication credentials were not provided.'})

    def test_fails_when_logged_user_not_supervisor(self):
        token = self._login_user('worker@gmail.com')
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token,
            }
        response = self.client.post(
            '/department/',
            {
                "name": "sales",
	            "manager": 1
            },
            **auth_headers
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, {"detail": "You do not have permission to perform this action."})

class DepartmentListApiViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454565",
            "phone_number": "+256782607610",
            "user_type": "Admin"
        }
        user = User.objects.create("admin@gmail.com", "password", **extra_fields)
        Department.objects.create(name='engineering', manager=user)

    def _login_user(self):
        token = self.client.post(
            '/token/',
            {
            "email":"admin@gmail.com",
            "password": "password"
        })
        res = token.content.decode('utf-8')
        dict_res = json.loads(res)
        return dict_res['access']

    def _make_decode_response(self, res):
        res = res.content.decode('utf-8')
        dict_res = json.loads(res)
        return dict_res

    def test_successfully_get_departments(self):
        token = self._login_user()
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token,
            }
        response = self.client.get(
            '/department/',
            **auth_headers
        )
        response = self._make_decode_response(response)
        self.assertEqual(response, [{"name":"engineering","manager":1}])

    def test_get_departments_fails_with_no_auth(self):
        token = self._login_user()
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token,
            }
        response = self.client.get(
            '/department/',
            # **auth_headers
        )
        response = self._make_decode_response(response)
        self.assertEqual(response, {'detail': 'Authentication credentials were not provided.'})


