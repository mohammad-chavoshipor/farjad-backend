"""
Services views for the Farjad ERP system.

This module contains views for service requests, technicians, and scheduling.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import ServiceRequest, ServiceType, Technician, ServiceNote, Schedule, ServiceRating
from .serializers import (
    ServiceRequestSerializer,
    ServiceTypeSerializer,
    TechnicianSerializer,
    ServiceNoteSerializer,
    ScheduleSerializer,
    ServiceRatingSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="List service requests", description="Retrieve a list of all service requests"),
    create=extend_schema(summary="Create service request", description="Create a new service request"),
    retrieve=extend_schema(summary="Get service request", description="Retrieve a specific service request"),
    update=extend_schema(summary="Update service request", description="Update a specific service request"),
    partial_update=extend_schema(summary="Partially update service request", description="Partially update a specific service request"),
    destroy=extend_schema(summary="Delete service request", description="Delete a specific service request"),
)
class ServiceRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing service requests."""
    
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'service_type', 'assigned_technician']
    search_fields = ['request_number', 'title', 'description', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['created_at', 'requested_date', 'scheduled_date', 'priority']
    ordering = ['-created_at']


@extend_schema_view(
    list=extend_schema(summary="List service types", description="Retrieve a list of all service types"),
    create=extend_schema(summary="Create service type", description="Create a new service type"),
    retrieve=extend_schema(summary="Get service type", description="Retrieve a specific service type"),
    update=extend_schema(summary="Update service type", description="Update a specific service type"),
    partial_update=extend_schema(summary="Partially update service type", description="Partially update a specific service type"),
    destroy=extend_schema(summary="Delete service type", description="Delete a specific service type"),
)
class ServiceTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing service types."""
    
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_price', 'created_at']
    ordering = ['name']


@extend_schema_view(
    list=extend_schema(summary="List technicians", description="Retrieve a list of all technicians"),
    create=extend_schema(summary="Create technician", description="Create a new technician"),
    retrieve=extend_schema(summary="Get technician", description="Retrieve a specific technician"),
    update=extend_schema(summary="Update technician", description="Update a specific technician"),
    partial_update=extend_schema(summary="Partially update technician", description="Partially update a specific technician"),
    destroy=extend_schema(summary="Delete technician", description="Delete a specific technician"),
)
class TechnicianViewSet(viewsets.ModelViewSet):
    """ViewSet for managing technicians."""
    
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['skill_level', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']
    ordering_fields = ['user__last_name', 'skill_level', 'created_at']
    ordering = ['user__last_name', 'user__first_name']


@extend_schema_view(
    list=extend_schema(summary="List schedules", description="Retrieve a list of all schedules"),
    create=extend_schema(summary="Create schedule", description="Create a new schedule"),
    retrieve=extend_schema(summary="Get schedule", description="Retrieve a specific schedule"),
    update=extend_schema(summary="Update schedule", description="Update a specific schedule"),
    partial_update=extend_schema(summary="Partially update schedule", description="Partially update a specific schedule"),
    destroy=extend_schema(summary="Delete schedule", description="Delete a specific schedule"),
)
class ScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing schedules."""
    
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['technician', 'is_confirmed']
    search_fields = ['technician__user__first_name', 'technician__user__last_name', 'notes']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['start_time']