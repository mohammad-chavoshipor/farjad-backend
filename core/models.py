"""
Core models for the Farjad ERP system.

This module contains the fundamental models that are used across the entire system.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

User = get_user_model()


class TimeStampedModel(models.Model):
    """Abstract base class with self-updating created and modified fields."""
    
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name=_('Created by')
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name=_('Updated by')
    )

    class Meta:
        abstract = True


class Contact(TimeStampedModel):
    """Contact information for customers, suppliers, and other entities."""
    
    CONTACT_TYPES = [
        ('customer', _('Customer')),
        ('supplier', _('Supplier')),
        ('employee', _('Employee')),
        ('other', _('Other')),
    ]
    
    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField(_('Last name'), max_length=100)
    email = models.EmailField(_('Email'), unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    phone = models.CharField(_('Phone'), validators=[phone_regex], max_length=17, blank=True)
    mobile = models.CharField(_('Mobile'), validators=[phone_regex], max_length=17, blank=True)
    contact_type = models.CharField(_('Contact type'), max_length=20, choices=CONTACT_TYPES)
    is_active = models.BooleanField(_('Is active'), default=True)
    notes = models.TextField(_('Notes'), blank=True)
    
    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['contact_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        """Return the full name of the contact."""
        return f"{self.first_name} {self.last_name}"


class Company(TimeStampedModel):
    """Company information for customers, suppliers, and partners."""
    
    COMPANY_TYPES = [
        ('customer', _('Customer')),
        ('supplier', _('Supplier')),
        ('partner', _('Partner')),
        ('competitor', _('Competitor')),
        ('other', _('Other')),
    ]
    
    name = models.CharField(_('Company name'), max_length=200, unique=True)
    legal_name = models.CharField(_('Legal name'), max_length=200, blank=True)
    company_type = models.CharField(_('Company type'), max_length=20, choices=COMPANY_TYPES)
    tax_id = models.CharField(_('Tax ID'), max_length=50, blank=True, unique=True, null=True)
    registration_number = models.CharField(_('Registration number'), max_length=50, blank=True)
    website = models.URLField(_('Website'), blank=True)
    email = models.EmailField(_('Email'), blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    fax = models.CharField(_('Fax'), max_length=20, blank=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    notes = models.TextField(_('Notes'), blank=True)
    
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['company_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class Address(TimeStampedModel):
    """Address information for contacts and companies."""
    
    ADDRESS_TYPES = [
        ('billing', _('Billing')),
        ('shipping', _('Shipping')),
        ('office', _('Office')),
        ('warehouse', _('Warehouse')),
        ('other', _('Other')),
    ]
    
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='addresses',
        verbose_name=_('Contact')
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='addresses',
        verbose_name=_('Company')
    )
    address_type = models.CharField(_('Address type'), max_length=20, choices=ADDRESS_TYPES)
    street_address = models.CharField(_('Street address'), max_length=255)
    city = models.CharField(_('City'), max_length=100)
    state = models.CharField(_('State/Province'), max_length=100)
    postal_code = models.CharField(_('Postal code'), max_length=20)
    country = models.CharField(_('Country'), max_length=100, default='Iran')
    is_primary = models.BooleanField(_('Is primary'), default=False)
    
    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ['-is_primary', 'city', 'street_address']
        indexes = [
            models.Index(fields=['contact']),
            models.Index(fields=['company']),
            models.Index(fields=['address_type']),
            models.Index(fields=['is_primary']),
        ]

    def __str__(self):
        entity = self.contact or self.company
        return f"{entity} - {self.street_address}, {self.city}"

    def clean(self):
        """Validate that either contact or company is provided, but not both."""
        from django.core.exceptions import ValidationError
        
        if not self.contact and not self.company:
            raise ValidationError(_('Either contact or company must be specified.'))
        
        if self.contact and self.company:
            raise ValidationError(_('Cannot specify both contact and company.'))


class SystemConfiguration(TimeStampedModel):
    """System-wide configuration settings."""
    
    key = models.CharField(_('Key'), max_length=100, unique=True)
    value = models.TextField(_('Value'))
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    
    class Meta:
        verbose_name = _('System Configuration')
        verbose_name_plural = _('System Configurations')
        ordering = ['key']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


class AuditLog(TimeStampedModel):
    """Audit log for tracking changes to important models."""
    
    ACTION_TYPES = [
        ('create', _('Create')),
        ('update', _('Update')),
        ('delete', _('Delete')),
        ('view', _('View')),
        ('login', _('Login')),
        ('logout', _('Logout')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('User')
    )
    action = models.CharField(_('Action'), max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(_('Model name'), max_length=100)
    object_id = models.CharField(_('Object ID'), max_length=100, blank=True)
    object_repr = models.CharField(_('Object representation'), max_length=200, blank=True)
    changes = models.JSONField(_('Changes'), default=dict, blank=True)
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    user_agent = models.TextField(_('User agent'), blank=True)
    
    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['model_name']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.created_at}"