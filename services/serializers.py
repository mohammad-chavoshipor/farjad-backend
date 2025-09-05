"""
Services serializers for the Farjad ERP system.

This module contains serializers for service requests, technicians, and scheduling.
"""

from rest_framework import serializers
from .models import ServiceRequest, ServiceType, Technician, ServiceNote, Schedule, ServiceRating


class ServiceTypeSerializer(serializers.ModelSerializer):
    """Serializer for ServiceType model."""
    
    class Meta:
        model = ServiceType
        fields = [
            'id',
            'name',
            'description',
            'base_price',
            'estimated_duration',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TechnicianSerializer(serializers.ModelSerializer):
    """Serializer for Technician model."""
    
    full_name = serializers.ReadOnlyField()
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Technician
        fields = [
            'id',
            'user',
            'full_name',
            'user_name',
            'user_email',
            'employee_id',
            'skill_level',
            'specializations',
            'hourly_rate',
            'is_available',
            'max_daily_hours',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceRequestSerializer(serializers.ModelSerializer):
    """Serializer for ServiceRequest model."""
    
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    customer_company_name = serializers.CharField(source='customer_company.name', read_only=True)
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    assigned_technician_name = serializers.CharField(source='assigned_technician.full_name', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'request_number',
            'title',
            'description',
            'customer',
            'customer_name',
            'customer_company',
            'customer_company_name',
            'service_type',
            'service_type_name',
            'priority',
            'status',
            'assigned_technician',
            'assigned_technician_name',
            'assigned_at',
            'assigned_by',
            'assigned_by_name',
            'requested_date',
            'scheduled_date',
            'started_at',
            'completed_at',
            'estimated_cost',
            'actual_cost',
            'service_address',
            'service_city',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'request_number', 'created_at', 'updated_at']


class ServiceNoteSerializer(serializers.ModelSerializer):
    """Serializer for ServiceNote model."""
    
    service_request_number = serializers.CharField(source='service_request.request_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = ServiceNote
        fields = [
            'id',
            'service_request',
            'service_request_number',
            'note',
            'is_internal',
            'created_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'created_at']


class ScheduleSerializer(serializers.ModelSerializer):
    """Serializer for Schedule model."""
    
    technician_name = serializers.CharField(source='technician.full_name', read_only=True)
    service_request_number = serializers.CharField(source='service_request.request_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id',
            'technician',
            'technician_name',
            'service_request',
            'service_request_number',
            'start_time',
            'end_time',
            'notes',
            'is_confirmed',
            'created_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'created_at']


class ServiceRatingSerializer(serializers.ModelSerializer):
    """Serializer for ServiceRating model."""
    
    service_request_number = serializers.CharField(source='service_request.request_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = ServiceRating
        fields = [
            'id',
            'service_request',
            'service_request_number',
            'rating',
            'comment',
            'created_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'created_at']
