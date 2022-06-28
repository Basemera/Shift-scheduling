from django.test import TestCase
import pytest
from rest_framework.test import APITestCase
import json
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
