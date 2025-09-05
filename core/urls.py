"""
Core app URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contacts', views.ContactViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'addresses', views.AddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', views.health_check, name='health-check'),
]
