import django_filters
from shift.models import Shift, WorkerSchedule
from shift.serializers import WorkerScheduleSerializer

class WorkerScheduleFilter(django_filters.FilterSet):
    department_name = django_filters.CharFilter(field_name='worker__department__name', lookup_expr='icontains')
    manager_email = django_filters.CharFilter(field_name='worker__department__manager__email', lookup_expr='icontains')
    user_email = django_filters.CharFilter(field_name='worker__user__email', lookup_expr='icontains')
    department_id = django_filters.CharFilter(field_name='worker__department__id')
    manager_id = django_filters.CharFilter(field_name='worker__department__manager__id')
    user_id = django_filters.CharFilter(field_name='worker__user__id')

    class Meta:
        model = WorkerSchedule
        fields = [
            'worker',
            'shift',
            'shift__shift_day',
            'shift__assigned_by',
            'shift__completed',
            'shift__full',
            'shift__time'
        ]