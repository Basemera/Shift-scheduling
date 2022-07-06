from django.urls import path
from .views import (
    ShiftCreateApiView,
    ShiftRetrieveUpdateDestroyAPIView,
    WorkerShceduleCreateListApiView,
    WorkScheduleRetrieveUpdateDestroyAPIView,
    WorkerScheduleSearchApiView,
    ShiftClockinAPIView
)

urlpatterns = [
    path('shift/', ShiftCreateApiView.as_view()),
    path('shift/<pk>', ShiftRetrieveUpdateDestroyAPIView.as_view()),
    path('worker/', WorkerShceduleCreateListApiView.as_view()),
    path('worker/<pk>', WorkScheduleRetrieveUpdateDestroyAPIView.as_view()),
    path('search/', WorkerScheduleSearchApiView.as_view()),
    path('<worker>/clockin/<shift>', ShiftClockinAPIView.as_view())
]