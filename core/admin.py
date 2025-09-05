"""
Core admin configuration for the Farjad ERP system.

This module contains admin configurations for core functionality.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, Company, Address, SystemConfiguration, AuditLog


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin configuration for Contact model."""
    
    list_display = [
        'full_name',
        'email',
        'phone',
        'contact_type',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'contact_type',
        'is_active',
        'created_at',
    ]
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'mobile',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'mobile')
        }),
        ('Classification', {
            'fields': ('contact_type', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin configuration for Company model."""
    
    list_display = [
        'name',
        'company_type',
        'email',
        'phone',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'company_type',
        'is_active',
        'created_at',
    ]
    search_fields = [
        'name',
        'legal_name',
        'email',
        'tax_id',
        'registration_number',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'legal_name', 'company_type')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'fax', 'website')
        }),
        ('Legal Information', {
            'fields': ('tax_id', 'registration_number')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin configuration for Address model."""
    
    list_display = [
        'get_entity_name',
        'address_type',
        'street_address',
        'city',
        'country',
        'is_primary',
    ]
    list_filter = [
        'address_type',
        'is_primary',
        'country',
        'created_at',
    ]
    search_fields = [
        'street_address',
        'city',
        'state',
        'postal_code',
        'contact__first_name',
        'contact__last_name',
        'company__name',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['city', 'street_address']
    
    def get_entity_name(self, obj):
        """Get the name of the associated entity."""
        if obj.contact:
            return obj.contact.full_name
        elif obj.company:
            return obj.company.name
        return 'N/A'
    get_entity_name.short_description = 'Entity'
    
    fieldsets = (
        ('Entity', {
            'fields': ('contact', 'company')
        }),
        ('Address Information', {
            'fields': ('address_type', 'street_address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Status', {
            'fields': ('is_primary',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    """Admin configuration for SystemConfiguration model."""
    
    list_display = [
        'key',
        'value_preview',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'created_at',
    ]
    search_fields = [
        'key',
        'description',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['key']
    
    def value_preview(self, obj):
        """Show a preview of the value."""
        if len(obj.value) > 50:
            return f"{obj.value[:50]}..."
        return obj.value
    value_preview.short_description = 'Value Preview'
    
    fieldsets = (
        ('Configuration', {
            'fields': ('key', 'value', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin configuration for AuditLog model."""
    
    list_display = [
        'user',
        'action',
        'model_name',
        'object_repr',
        'ip_address',
        'created_at',
    ]
    list_filter = [
        'action',
        'model_name',
        'created_at',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'object_repr',
        'ip_address',
    ]
    readonly_fields = [
        'user',
        'action',
        'model_name',
        'object_id',
        'object_repr',
        'changes',
        'ip_address',
        'user_agent',
        'created_at',
    ]
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        """Disable adding new audit logs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing audit logs."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Disable deleting audit logs."""
        return False