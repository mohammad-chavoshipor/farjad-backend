"""
Services app URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'requests', views.ServiceRequestViewSet)
router.register(r'types', views.ServiceTypeViewSet)
router.register(r'technicians', views.TechnicianViewSet)
router.register(r'schedules', views.ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
