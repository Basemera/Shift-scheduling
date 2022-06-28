import json
from django.db import IntegrityError
from django.test import TestCase
import pytest
import json
from rest_framework.test import APITestCase

from .models import Worker

from users.models import User
from department.models import Department

# Create your tests here.
@pytest.mark.django_db()
class WorkerModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_create_worker_successful(self):
        dept = Department.objects.filter(name='Engineering').first()
        user = User.objects.filter(email='worker@gmail.com').first()
        worker = Worker.objects.create(user=user, department=dept)
        self.assertEqual(worker.user, user)
        self.assertEqual(worker.department, dept)

    def test_create_worker_unsuccessful_when_fields_missing(self):
        dept = Department.objects.filter(name='engineering').first()
        user = User.objects.filter(email='worker@gmail.com').first()
        with pytest.raises(IntegrityError, match='null value in column "department_id" of relation "worker_worker" violates not-null') as excInfo:
            worker = Worker.objects.create(user=user, department=None)


@pytest.mark.django_db()
class WorkerCreateApiViewTest(APITestCase):
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

    def test_successfully_create_worker(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/worker/',
            {
	            "user": 3,
	            "department": 1
            },
        )
        self.assertEqual(response.data, {
            "user": 3,
            "department": 1
        })

    def test_unsuccessfully_with_no_auth(self):
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
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/worker/',
            {
	            "user": 1,
	            "department": 1
            },
        )
        dict_res = self._make_decode_response(response)
        self.assertEqual(dict_res, {"detail": "You do not have permission to perform this action."})

@pytest.mark.django_db()
class WorkerListApiViewTest(APITestCase):
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


    def test_successfully_get_workers(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/worker/',
        )
        response = self._make_decode_response(response)
        self.assertEqual(response, [{"user":3,"department":1}])

@pytest.mark.django_db()
class WorkerRetrieveUpdateDestroyAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()
    def test_get_worker(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/worker/1'
        )
        self.assertEqual(
            response.data,
            {
                "department": 1,
	            "user": 3
            }
        )
        
    def test_update_worker_succesful(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        old_worker = Worker.objects.get(pk=1)

        response = self.client.put(
            '/worker/1',
            {
               "user": 3,
	            "department": 2
            },
            format='json'
        )
        worker = Worker.objects.get(pk=1)
        self.assertEqual(worker.department.id, 2)
        self.assertNotEqual(worker.department.id, old_worker.department.id)

    # def test_update_worker_unsuccesful_when_user_not_supervisor(self):
    #     user = User.objects.get(pk=3)
    #     self.client.force_authenticate(user)

    #     response = self.client.put(
    #         '/worker/1',
    #         {
    #            "user": 3,
	#             "department": 2
    #         },
    #         format='json'
    #     )
    #     res = response.content.decode('utf-8')
    #     dict_res = json.loads(res)
    #     self.assertEqual(dict_res, 
    #         {
    #             "detail":"You do not have permission to perform this action."
    #         }
    #     )
    def test_delete_worker_succesful_when_user_supervisor(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.delete(
            '/worker/1',
            format='json'
        )
        worker = Worker.objects.filter(pk=1)
        self.assertEqual(len(worker), 0)

