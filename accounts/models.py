"""
User account models for the Farjad ERP system.

This module contains user-related models including profiles, roles, and permissions.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Extended User model with additional fields."""
    
    email = models.EmailField(_('Email address'), unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    phone = models.CharField(_('Phone'), validators=[phone_regex], max_length=17, blank=True)
    is_verified = models.BooleanField(_('Is verified'), default=False)
    last_login_ip = models.GenericIPAddressField(_('Last login IP'), null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    """Extended user profile with additional information."""
    
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )
    avatar = models.ImageField(_('Avatar'), upload_to='avatars/', blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    bio = models.TextField(_('Bio'), blank=True)
    address = models.TextField(_('Address'), blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    country = models.CharField(_('Country'), max_length=100, default='Iran')
    postal_code = models.CharField(_('Postal code'), max_length=20, blank=True)
    emergency_contact_name = models.CharField(_('Emergency contact name'), max_length=100, blank=True)
    emergency_contact_phone = models.CharField(
        _('Emergency contact phone'),
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        )],
        max_length=17,
        blank=True
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f"{self.user.full_name} Profile"


class Role(models.Model):
    """Role model for role-based access control."""
    
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    # Permissions
    permissions = models.ManyToManyField(
        'auth.Permission',
        through='RolePermission',
        related_name='roles',
        verbose_name=_('Permissions')
    )

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name']

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    """Through model for Role and Permission many-to-many relationship."""
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name=_('Role'))
    permission = models.ForeignKey(
        'auth.Permission',
        on_delete=models.CASCADE,
        verbose_name=_('Permission')
    )
    granted = models.BooleanField(_('Granted'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Role Permission')
        verbose_name_plural = _('Role Permissions')
        unique_together = ['role', 'permission']

    def __str__(self):
        status = 'Granted' if self.granted else 'Denied'
        return f"{self.role.name} - {self.permission.name} ({status})"


class UserRole(models.Model):
    """Through model for User and Role many-to-many relationship."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name=_('Role'))
    assigned_at = models.DateTimeField(_('Assigned at'), auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_roles',
        verbose_name=_('Assigned by')
    )
    is_active = models.BooleanField(_('Is active'), default=True)

    class Meta:
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user.full_name} - {self.role.name}"


class UserSession(models.Model):
    """Track user sessions for security and analytics."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    session_key = models.CharField(_('Session key'), max_length=40, unique=True)
    ip_address = models.GenericIPAddressField(_('IP address'))
    user_agent = models.TextField(_('User agent'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_activity = models.DateTimeField(_('Last activity'), auto_now=True)
    is_active = models.BooleanField(_('Is active'), default=True)

    class Meta:
        verbose_name = _('User Session')
        verbose_name_plural = _('User Sessions')
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
            models.Index(fields=['is_active']),
            models.Index(fields=['last_activity']),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.session_key}"


class PasswordResetToken(models.Model):
    """Password reset tokens for secure password reset functionality."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    token = models.CharField(_('Token'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    expires_at = models.DateTimeField(_('Expires at'))
    is_used = models.BooleanField(_('Is used'), default=False)
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)

    class Meta:
        verbose_name = _('Password Reset Token')
        verbose_name_plural = _('Password Reset Tokens')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['token']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['is_used']),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.token[:10]}..."

    def is_expired(self):
        """Check if the token has expired."""
        from django.utils import timezone
        return timezone.now() > self.expires_at