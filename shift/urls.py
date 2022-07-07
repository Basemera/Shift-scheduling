from django.urls import path
from .views import (
    ShiftCreateApiView,
    ShiftRetrieveUpdateDestroyAPIView,
    WorkerShceduleCreateListApiView,
    WorkScheduleRetrieveUpdateDestroyAPIView,
    WorkerScheduleSearchApiView,
    ShiftClockinAPIView,
    WorkerScheduleWorkerLogHoursApiView,
    WorkerScheduleDownloadApiView
)

urlpatterns = [
    path('shift/', ShiftCreateApiView.as_view()),
    path('shift/<pk>', ShiftRetrieveUpdateDestroyAPIView.as_view()),
    path('worker/', WorkerShceduleCreateListApiView.as_view()),
    path('worker/<pk>', WorkScheduleRetrieveUpdateDestroyAPIView.as_view()),
    path('search/', WorkerScheduleSearchApiView.as_view()),
    path('<worker>/clockin/<shift>', ShiftClockinAPIView.as_view()),
    path('hours/', WorkerScheduleWorkerLogHoursApiView.as_view()),
    path('download/', WorkerScheduleDownloadApiView.as_view())
]
