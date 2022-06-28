from django.test import TestCase
from django.db import IntegrityError
import pytest
import json
from rest_framework.test import force_authenticate
from .views import ListCreateAPIView
from rest_framework.test import APITestCase

# Create your tests here.
from users.models import User
from .models import Department

@pytest.mark.django_db()
class DepartmentModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_create_department_successful(self):
        user = User.objects.filter(email='admin@gmail.com').first()
        dept = Department.objects.create(name='technology', manager=user)
        self.assertEqual(dept.name, 'technology')
        self.assertEqual(dept.manager, user)

    def test_create_user_unsuccesful_with_missing_field(self):
        user = User.objects.filter(email='admin@gmail.com').first()
        with pytest.raises(IntegrityError, match='null value in column "name"') as excInfo:
            dept = Department.objects.create(name=None, manager=user)

        

@pytest.mark.django_db()
class DepartmentCreateApiViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

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
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/department/',
            {
                "name": "sales",
	            "manager": 1
            },
            format='json'
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
            format='json'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, {'detail': 'Authentication credentials were not provided.'})

    def test_fails_when_logged_user_not_supervisor(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/department/',
            {
                "name": "sales",
	            "manager": 1
            },
            format='json'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, {"detail": "You do not have permission to perform this action."})

@pytest.mark.django_db()
class DepartmentListApiViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

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
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/department/',
            format='json'
        )
        name, manager = response.data[0].items()
        
        self.assertEqual(name, ('name', 'Engineering'))
        self.assertEqual(manager, ('manager', 2))

    def test_get_departments_fails_with_no_auth(self):
        response = self.client.get(
            '/department/',
        )
        response = self._make_decode_response(response)
        self.assertEqual(response, {'detail': 'Authentication credentials were not provided.'})

@pytest.mark.django_db()
class DepartmentRetrieveUpdateDestroyAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()
    def test_get_department(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/department/1/'
        )
        self.assertEqual(
            response.data,
            {
                "name": "Engineering",
	            "manager": 2
            }
        )
        
    def test_update_department_succesful(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)

        response = self.client.put(
            '/department/1/',
            {
                "name": "P&E",
                "manager": 2
            },
            format='json'
        )
        dept = Department.objects.get(pk=1)
        self.assertEqual(dept.name, 'P&E')

    def test_update_department_unsuccesful_when_user_not_supervisor(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)

        response = self.client.put(
            '/department/1/',
            {
                "name": "P&E",
                "manager": 2
            },
            format='json'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, 
            {
                "detail":"You do not have permission to perform this action."
            }
        )