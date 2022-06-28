from django.test import TestCase
import pytest
from rest_framework.test import APITestCase
import json
from shift.models import Shift
from users.models import User
# Create your tests here.
pytest.mark.django_db()
class ShiftCreateApiViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_create_shift_successful(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/schedule/shift/',
            {
                "time": 1,
                "shift_day": "2022-07-28",
                "completed": False,
                "full": False
            },
            format='json'
        )
        self.assertEquals(response.data, 
            {
                'assigned_by': user.id,
                'completed': False,
                'shift_day': '2022-07-28',
                'time': 1,
                'full': False
            }
        )

    def test_create_shift_unsuccessful_with_missing_fields(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/schedule/shift/',
            {
                "time": 1,
                "completed": False,
                "full": False
            },
            format='json'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, 
            {
                "shift_day":["This field is required."]
            }
        )

    def test_create_shift_unsuccessful_with_authenticated_user_not_supervisor(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/schedule/shift/',
            {
                "time": 1,
                "shift_day": "2022-07-28",
                "completed": False,
                "full": False
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

@pytest.mark.django_db()
class ShiftRetrieveUpdateDestroyAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        
        return super().setUpTestData()

    def test_get_single_shift(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/schedule/shift/1'
        )
        self.assertEqual(response.data, {
            "assigned_by":2,
            "completed":False,
            "shift_day":"2022-06-28",
            "time":1,
            "full":False,
            "id":1
        })

    def test_edit_single_shift(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/shift/1',
            {
                "time": 1,
                "shift_day": "2022-07-28",
                "completed": True,
                "full": False
            },
            format='json'
        )
        self.assertEqual(response.data, {
            "completed":True,
            "shift_day":"2022-07-28",
            "time":1,
            "full":False,
            "id":1
        })

    def test_update_shift_unsuccessful_with_authenticated_user_not_supervisor(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/shift/1',
            {
                "time": 1,
                "shift_day": "2022-07-28",
                "completed": True,
                "full": False
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

    def test_delete_shift_succesful_when_user_supervisor(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.delete(
            '/schedule/shift/1',
            format='json'
        )
        shift = Shift.objects.filter(pk=1)
        self.assertEqual(len(shift), 0)

@pytest.mark.django_db()
class TestWorkerSchedule(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_bulk_create_schedule(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/schedule/worker/',
            {
                "worker": [3,4],
	            "shift":1
            },
            format='json'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, [
            {
            "worker": 3,
            "shift": 1
            },
            {
            "worker": 4,
            "shift": 1
            }
        ])

    def test_bulk_create_fails_if_details_inaccurate(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.post(
            '/schedule/worker/',
            {
                "worker": [3,44,45],
	            "shift":1
            },
            format='json'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res[1], {
            'worker': ['Invalid pk "44" - object does not exist.']
        })
