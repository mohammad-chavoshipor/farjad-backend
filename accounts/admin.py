"""
Accounts admin configuration for the Farjad ERP system.

This module contains admin configurations for user management and authentication.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Profile, Role, RolePermission, UserRole, UserSession, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_verified',
        'date_joined',
    ]
    list_filter = [
        'is_active',
        'is_verified',
        'is_staff',
        'is_superuser',
        'date_joined',
    ]
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'last_login_ip')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model."""
    
    list_display = [
        'user',
        'gender',
        'city',
        'country',
        'created_at',
    ]
    list_filter = [
        'gender',
        'country',
        'created_at',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'city',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['user__last_name', 'user__first_name']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('avatar', 'gender', 'date_of_birth', 'bio')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin configuration for Role model."""
    
    list_display = [
        'name',
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
        ('Role Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """Admin configuration for RolePermission model."""
    
    list_display = [
        'role',
        'permission',
        'granted',
        'created_at',
    ]
    list_filter = [
        'granted',
        'role',
        'permission__content_type',
        'created_at',
    ]
    search_fields = [
        'role__name',
        'permission__name',
        'permission__codename',
    ]
    readonly_fields = [
        'created_at',
    ]
    ordering = ['role__name', 'permission__name']
    
    fieldsets = (
        ('Permission Assignment', {
            'fields': ('role', 'permission', 'granted')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """Admin configuration for UserRole model."""
    
    list_display = [
        'user',
        'role',
        'is_active',
        'assigned_at',
        'assigned_by',
    ]
    list_filter = [
        'is_active',
        'role',
        'assigned_at',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'role__name',
    ]
    readonly_fields = [
        'assigned_at',
    ]
    ordering = ['user__last_name', 'role__name']
    
    fieldsets = (
        ('Role Assignment', {
            'fields': ('user', 'role', 'is_active')
        }),
        ('Assignment Information', {
            'fields': ('assigned_at', 'assigned_by')
        }),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin configuration for UserSession model."""
    
    list_display = [
        'user',
        'ip_address',
        'is_active',
        'created_at',
        'last_activity',
    ]
    list_filter = [
        'is_active',
        'created_at',
        'last_activity',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'ip_address',
        'session_key',
    ]
    readonly_fields = [
        'session_key',
        'created_at',
        'last_activity',
    ]
    ordering = ['-last_activity']
    
    def has_add_permission(self, request):
        """Disable adding new sessions."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing sessions."""
        return False


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin configuration for PasswordResetToken model."""
    
    list_display = [
        'user',
        'token_preview',
        'is_used',
        'created_at',
        'expires_at',
    ]
    list_filter = [
        'is_used',
        'created_at',
        'expires_at',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'token',
    ]
    readonly_fields = [
        'token',
        'created_at',
    ]
    ordering = ['-created_at']
    
    def token_preview(self, obj):
        """Show a preview of the token."""
        return f"{obj.token[:10]}..."
    token_preview.short_description = 'Token Preview'
    
    def has_add_permission(self, request):
        """Disable adding new tokens."""
        return False