import json
from django.db import IntegrityError
from django.test import TestCase
import pytest
import json

from .models import Worker

from users.models import User
from department.models import Department

# Create your tests here.
class WorkerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454565",
            "phone_number": "+256782607610",
            "user_type": "Supervisor"
        }
        user = User.objects.create("admin@gmail.com", "password", **extra_fields)

        dept_fields = {
            'name': 'engineering',
            'manager': user
        }
        dept = Department.objects.create(**dept_fields)

        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343453565",
            "phone_number": "+256782607620",
            "user_type": "Worker"
        }
        user = User.objects.create("worker@gmail.com", "password", **extra_fields)

    def test_create_worker_successful(self):
        dept = Department.objects.filter(name='engineering').first()
        user = User.objects.filter(email='worker@gmail.com').first()
        worker = Worker.objects.create(user=user, department=dept)
        self.assertEqual(worker.user, user)
        self.assertEqual(worker.department, dept)

    def test_create_worker_unsuccessful_when_fields_missing(self):
        dept = Department.objects.filter(name='engineering').first()
        user = User.objects.filter(email='worker@gmail.com').first()
        with pytest.raises(IntegrityError, match='null value in column "department_id" of relation "worker_worker" violates not-null') as excInfo:
            worker = Worker.objects.create(user=user, department=None)


class WorkerCreateApiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454565",
            "phone_number": "+256782607610",
            "user_type": "Supervisor"
        }
        user = User.objects.create("admin@gmail.com", "password", **extra_fields)

        dept_fields = {
            'name': 'engineering',
            'manager': user
        }
        dept = Department.objects.create(**dept_fields)

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

    def test_successfully_create_worker(self):
        token = self._login_user()
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token,
        }
        response = self.client.post(
            '/worker/',
            {
	            "user": 1,
	            "department": 1
            },
            **auth_headers
        )
        dict_res = self._make_decode_response(response)
        self.assertEqual(dict_res, {
            "user": 1,
            "department": 1
        })

    def test_unsuccessfully_with_no_auth(self):
        token = self._login_user()
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token,
        }
        response = self.client.post(
            '/worker/',
            {
	            "user": 1,
	            "department": 1
            },
        )
        dict_res = self._make_decode_response(response)
        self.assertEqual(dict_res, {'detail': 'Authentication credentials were not provided.'})

    def test_unsuccessfully_when_logged_in_not_supervisor(self):
        token = self._login_user('worker@gmail.com')
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token,
        }
        response = self.client.post(
            '/worker/',
            {
	            "user": 1,
	            "department": 1
            },
            **auth_headers
        )
        dict_res = self._make_decode_response(response)
        self.assertEqual(dict_res, {"detail": "You do not have permission to perform this action."})

class WorkerListApiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        extra_fields = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454565",
            "phone_number": "+256782607610",
            "user_type": "Supervisor"
        }
        user = User.objects.create("admin@gmail.com", "password", **extra_fields)

        dept_fields = {
            'name': 'engineering',
            'manager': user
        }
        dept = Department.objects.create(**dept_fields)

        extra_fields2 = {
            "first_name": "Phiona",
            "last_name": "Basemera",
            "nin": "12343454465",
            "phone_number": "+256772607610",
            "user_type": "Worker"
        }
        user1 = User.objects.create("worker@gmail.com", "password", **extra_fields2)
        Worker.objects.create(department=dept,user=user1)
   
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


    def test_successfully_get_workers(self):
        token = self._login_user('worker@gmail.com')
        auth_headers = {
            'HTTP_AUTHORIZATION': "Bearer " + token,
        }
        response = self.client.get(
            '/worker/',
            **auth_headers
        )
        response = self._make_decode_response(response)
        self.assertEqual(response, [{"user":2,"department":1}])
