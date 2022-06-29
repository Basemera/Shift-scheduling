import pytest

from django.core.management import call_command

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'fixtures/users.json')
        call_command('loaddata', 'fixtures/department.json')
        call_command('loaddata', 'fixtures/worker.json')
        call_command('loaddata', 'fixtures/time.json')
        call_command('loaddata', 'fixtures/shifts.json')
        call_command('loaddata', 'fixtures/worker_schedule.json')