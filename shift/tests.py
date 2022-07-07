from django.test import TestCase
import pytest
from rest_framework.test import APITestCase
import json
from shift.models import Shift, WorkerSchedule
from users.models import User
import datetime
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
                "full": False,
            },
            format='json'
        )
        self.assertEquals(response.data, 
            {
                'assigned_by': user.id,
                'completed': False,
                'shift_day': '2022-07-28',
                'time': 1,
                'full': False,
                "id": 3
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
            "time":2,
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
            '/schedule/shift/3',
            format='json'
        )
        shift = Shift.objects.filter(pk=3)
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

@pytest.mark.django_db()
class TestWorkScheduleRetrieveUpdateDestroyAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_retrieve_worker_schedule(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/schedule/worker/1'
        )
        self.assertEqual(response.data, {
            "worker": 1,
            "shift": 1,
            "clocked_in": None,
            "clocked_out": None
        })

    def test_update_worker_schedule_fails_when_clocked_in_none(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/worker/1',
            {
                "worker":3,
                "shift":1,
                "clocked_in": None,
                "clocked_out": "2022-06-28"
            },
            format='json'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, 
            {
                "non_field_errors": [
                        "Clocking out cannot happen before clocking in."
                    ]
            }
        )

    def test_update_worker_schedule_clockin_successful(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/worker/1',
            {
                "worker":3,
                "shift":1,
                "clocked_in": '2022-06-28',
                "clocked_out": None
            },
            format='json'
        )
        date = datetime.datetime.strptime('2022-06-28 00:00:00', '%Y-%m-%d %H:%M:%S')
        
        self.assertEqual(response.data, {
            "worker": 3,
            "shift": 1,
            "clocked_in": '2022-06-28T00:00:00Z',
            "clocked_out": None
        })

    def test_update_worker_schedule_clockout_successful(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/worker/1',
            {
                "worker":3,
                "shift":1,
                "clocked_in": '2022-06-28',
                "clocked_out": '2022-06-28'
            },
            format='json'
        )
        date = datetime.datetime.strptime('2022-06-28 00:00:00', '%Y-%m-%d %H:%M:%S')
        
        self.assertEqual(response.data, {
            "worker": 3,
            "shift": 1,
            "clocked_in": '2022-06-28T00:00:00Z',
            "clocked_out": '2022-06-28T00:00:00Z'
        })

    def test_delete_worker_schedule_succesful_when_user_supervisor(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.delete(
            '/schedule/worker/1',
            format='json'
        )
        schedule = WorkerSchedule.objects.filter(pk=1)
        self.assertEqual(len(schedule), 0)

    def test_delete_worker_schedule_unsuccesful_when_shift_completed(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        shift = Shift.objects.get(pk=1)
        shift.completed = True
        shift.save()
        response = self.client.delete(
            '/schedule/worker/1',
            format='json'
        )
        schedule = WorkerSchedule.objects.filter(pk=1)
        self.assertEqual(len(schedule), 1)
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, 
            {
                "message":"Cannot delete an entry from a completed shift"
            }
        )


class WorkerScheduleSearchApiViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()
    def test_search_successful(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/schedule/search/?department_name=Engineering'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        # print(dict_res)
        for result in dict_res:
            self.assertEqual(
                json.loads((result['worker']))['department'],
                'Engineering'
            )

    def test_search_successful_with_multiple_filters(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/schedule/search/?department_name=Engineering&shift_completed=true'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        for result in dict_res:
            self.assertEqual(
                json.loads((result['worker']))['department'],
                'Engineering'
            )
            self.assertEqual(
                json.loads((result['shift']))['completed'],
                True
            )

    def test_search_returns_empty_with_unsupported_filter_fields(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/schedule/search/?unsupporetd_field=say'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, [])

    def test_search_returns_empty_when_no_fields_passed_in(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            '/schedule/search/'
        )
        res = response.content.decode('utf-8')
        dict_res = json.loads(res)
        self.assertEqual(dict_res, [])

class WorkerScheduleDownloadApiViewTest(APITestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_successful_download(self):
        response = self.client.get(
            '/schedule/download/?department_name=Engineering'
        )

        self.assertEqual(
            response.get('Content-Disposition'), 'attachment; filename="worker_schedule.csv"'
        )

class ShiftClockinAPIViewTest(APITestCase):
    def setUp(self) -> None:
        return super().setUp()

    @pytest.mark.freeze_time('2022-06-28')
    def test_successful_clockin(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/1/clockin/1',
            {
                "action": "clockin"
            },
            format='json'
        )
        
        data = {
            "shift":1,
            "worker":1,
            "clocked_in": '2022-06-27T08:00:00Z',
            "clocked_out": None
        }

        self.assertEqual(response.data, data)

    @pytest.mark.freeze_time('2022-06-26')
    def test_unsuccessful_clockin_when_shift_has_not_started(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/1/clockin/1',
            {
                "action": "clockin"
            },
            format='json'
        )
        self.assertEqual(response.data, {'message': 'Cannot clockin to shift that has not started'})

    
    @pytest.mark.freeze_time('2022-07-29')
    def test_successful_clockout(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/1/clockin/2',
            {
                "action": "clockout"
            },
            format='json'
        )
        
        data = {
            "shift":2,
            "worker":1,
            "clocked_in": '2022-07-27T00:00:00Z',
            "clocked_out": '2022-07-27T08:00:00Z'
        }
        self.assertEqual(response.data, data)

    @pytest.mark.freeze_time('2022-06-26')
    def test_unsuccessful_clockout_when_shift_has_not_started(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/1/clockin/1',
            {
                "action": "clockout"
            },
            format='json'
        )
        self.assertEqual(response.data, {'message': 'Cannot clockout to shift that has not started'})

    def test_unsuccessful_with_invalid_input(self):
        user = User.objects.get(pk=3)
        self.client.force_authenticate(user)
        response = self.client.put(
            '/schedule/1/clockin/1',
            {
                "action": "logs"
            },
            format='json'
        )
        self.assertEqual(response.data, {'message': 'Missing required arguments'})
