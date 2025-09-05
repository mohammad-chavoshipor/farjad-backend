"""
Services admin configuration for the Farjad ERP system.

This module contains admin configurations for service requests, technicians, and scheduling.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceRequest, ServiceType, Technician, ServiceNote, Schedule, ServiceRating


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    """Admin configuration for ServiceType model."""
    
    list_display = [
        'name',
        'base_price',
        'estimated_duration',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'created_at',
    ]
    search_fields = [
        'name',
        'description',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['name']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'base_price', 'estimated_duration', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    """Admin configuration for Technician model."""
    
    list_display = [
        'user',
        'employee_id',
        'skill_level',
        'hourly_rate',
        'is_available',
        'created_at',
    ]
    list_filter = [
        'skill_level',
        'is_available',
        'created_at',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'employee_id',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['user__last_name', 'user__first_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'employee_id', 'skill_level')
        }),
        ('Specializations', {
            'fields': ('specializations',)
        }),
        ('Work Information', {
            'fields': ('hourly_rate', 'is_available', 'max_daily_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Admin configuration for ServiceRequest model."""
    
    list_display = [
        'request_number',
        'title',
        'customer',
        'service_type',
        'priority',
        'status',
        'assigned_technician',
        'scheduled_date',
        'created_at',
    ]
    list_filter = [
        'status',
        'priority',
        'service_type',
        'assigned_technician',
        'created_at',
        'scheduled_date',
    ]
    search_fields = [
        'request_number',
        'title',
        'description',
        'customer__first_name',
        'customer__last_name',
        'customer__email',
    ]
    readonly_fields = [
        'request_number',
        'created_at',
        'updated_at',
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('request_number', 'title', 'description')
        }),
        ('Customer Information', {
            'fields': ('customer', 'customer_company')
        }),
        ('Service Details', {
            'fields': ('service_type', 'priority', 'status')
        }),
        ('Assignment', {
            'fields': ('assigned_technician', 'assigned_at', 'assigned_by')
        }),
        ('Scheduling', {
            'fields': ('requested_date', 'scheduled_date', 'started_at', 'completed_at')
        }),
        ('Pricing', {
            'fields': ('estimated_cost', 'actual_cost')
        }),
        ('Location', {
            'fields': ('service_address', 'service_city')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ServiceNote)
class ServiceNoteAdmin(admin.ModelAdmin):
    """Admin configuration for ServiceNote model."""
    
    list_display = [
        'service_request',
        'note_preview',
        'is_internal',
        'created_at',
        'created_by',
    ]
    list_filter = [
        'is_internal',
        'created_at',
    ]
    search_fields = [
        'service_request__request_number',
        'service_request__title',
        'note',
    ]
    readonly_fields = [
        'created_at',
    ]
    ordering = ['-created_at']
    
    def note_preview(self, obj):
        """Show a preview of the note."""
        if len(obj.note) > 50:
            return f"{obj.note[:50]}..."
        return obj.note
    note_preview.short_description = 'Note Preview'
    
    fieldsets = (
        ('Note Information', {
            'fields': ('service_request', 'note', 'is_internal')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Admin configuration for Schedule model."""
    
    list_display = [
        'technician',
        'service_request',
        'start_time',
        'end_time',
        'is_confirmed',
        'created_at',
    ]
    list_filter = [
        'is_confirmed',
        'start_time',
        'created_at',
    ]
    search_fields = [
        'technician__user__first_name',
        'technician__user__last_name',
        'service_request__request_number',
        'service_request__title',
    ]
    readonly_fields = [
        'created_at',
    ]
    ordering = ['start_time']
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('technician', 'service_request', 'start_time', 'end_time', 'is_confirmed')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ServiceRating)
class ServiceRatingAdmin(admin.ModelAdmin):
    """Admin configuration for ServiceRating model."""
    
    list_display = [
        'service_request',
        'rating',
        'created_at',
        'created_by',
    ]
    list_filter = [
        'rating',
        'created_at',
    ]
    search_fields = [
        'service_request__request_number',
        'service_request__title',
        'comment',
    ]
    readonly_fields = [
        'created_at',
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Rating Information', {
            'fields': ('service_request', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )