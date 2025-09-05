"""
Services models for the Farjad ERP system.

This module contains service request, technician, and scheduling models.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

User = get_user_model()


class ServiceType(models.Model):
    """Service type model for categorizing services."""
    
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    base_price = models.DecimalField(
        _('Base price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    estimated_duration = models.DurationField(_('Estimated duration'))
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Service Type')
        verbose_name_plural = _('Service Types')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class Technician(models.Model):
    """Technician model for service technicians."""
    
    SKILL_LEVELS = [
        ('junior', _('Junior')),
        ('intermediate', _('Intermediate')),
        ('senior', _('Senior')),
        ('expert', _('Expert')),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='technician_profile',
        verbose_name=_('User')
    )
    employee_id = models.CharField(_('Employee ID'), max_length=50, unique=True)
    skill_level = models.CharField(_('Skill level'), max_length=20, choices=SKILL_LEVELS)
    specializations = models.ManyToManyField(
        ServiceType,
        related_name='technicians',
        verbose_name=_('Specializations')
    )
    hourly_rate = models.DecimalField(
        _('Hourly rate'),
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    is_available = models.BooleanField(_('Is available'), default=True)
    max_daily_hours = models.PositiveIntegerField(_('Max daily hours'), default=8)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Technician')
        verbose_name_plural = _('Technicians')
        ordering = ['user__last_name', 'user__first_name']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['skill_level']),
            models.Index(fields=['is_available']),
        ]

    def __str__(self):
        return f"{self.user.full_name} ({self.employee_id})"

    @property
    def full_name(self):
        """Return the full name of the technician."""
        return self.user.full_name


class ServiceRequest(models.Model):
    """Service request model for customer service requests."""
    
    PRIORITY_LEVELS = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('assigned', _('Assigned')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('on_hold', _('On Hold')),
    ]
    
    # Basic Information
    request_number = models.CharField(_('Request number'), max_length=50, unique=True)
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    
    # Customer Information
    customer = models.ForeignKey(
        'core.Contact',
        on_delete=models.PROTECT,
        related_name='service_requests',
        verbose_name=_('Customer')
    )
    customer_company = models.ForeignKey(
        'core.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_requests',
        verbose_name=_('Customer company')
    )
    
    # Service Details
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.PROTECT,
        related_name='service_requests',
        verbose_name=_('Service type')
    )
    priority = models.CharField(_('Priority'), max_length=20, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Assignment
    assigned_technician = models.ForeignKey(
        Technician,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests',
        verbose_name=_('Assigned technician')
    )
    assigned_at = models.DateTimeField(_('Assigned at'), null=True, blank=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests',
        verbose_name=_('Assigned by')
    )
    
    # Scheduling
    requested_date = models.DateTimeField(_('Requested date'), null=True, blank=True)
    scheduled_date = models.DateTimeField(_('Scheduled date'), null=True, blank=True)
    started_at = models.DateTimeField(_('Started at'), null=True, blank=True)
    completed_at = models.DateTimeField(_('Completed at'), null=True, blank=True)
    
    # Pricing
    estimated_cost = models.DecimalField(
        _('Estimated cost'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    actual_cost = models.DecimalField(
        _('Actual cost'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Location
    service_address = models.TextField(_('Service address'), blank=True)
    service_city = models.CharField(_('Service city'), max_length=100, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_service_requests',
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Service Request')
        verbose_name_plural = _('Service Requests')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['request_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_technician']),
            models.Index(fields=['scheduled_date']),
        ]

    def __str__(self):
        return f"{self.request_number} - {self.title}"

    def save(self, *args, **kwargs):
        """Generate request number if not provided."""
        if not self.request_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.request_number = f"SR-{timestamp}"
        super().save(*args, **kwargs)


class ServiceNote(models.Model):
    """Service note model for tracking service progress."""
    
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name=_('Service request')
    )
    note = models.TextField(_('Note'))
    is_internal = models.BooleanField(_('Is internal'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Service Note')
        verbose_name_plural = _('Service Notes')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['service_request']),
            models.Index(fields=['is_internal']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.service_request.request_number} - Note {self.id}"


class Schedule(models.Model):
    """Schedule model for technician scheduling."""
    
    technician = models.ForeignKey(
        Technician,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_('Technician')
    )
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_('Service request')
    )
    start_time = models.DateTimeField(_('Start time'))
    end_time = models.DateTimeField(_('End time'))
    notes = models.TextField(_('Notes'), blank=True)
    is_confirmed = models.BooleanField(_('Is confirmed'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['technician']),
            models.Index(fields=['service_request']),
            models.Index(fields=['start_time']),
            models.Index(fields=['is_confirmed']),
        ]

    def __str__(self):
        return f"{self.technician.full_name} - {self.service_request.request_number}"

    def clean(self):
        """Validate schedule times."""
        from django.core.exceptions import ValidationError
        
        if self.start_time >= self.end_time:
            raise ValidationError(_('End time must be after start time.'))


class ServiceRating(models.Model):
    """Service rating model for customer feedback."""
    
    RATING_CHOICES = [
        (1, _('1 - Very Poor')),
        (2, _('2 - Poor')),
        (3, _('3 - Average')),
        (4, _('4 - Good')),
        (5, _('5 - Excellent')),
    ]
    
    service_request = models.OneToOneField(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='rating',
        verbose_name=_('Service request')
    )
    rating = models.PositiveIntegerField(
        _('Rating'),
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(_('Comment'), blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Service Rating')
        verbose_name_plural = _('Service Ratings')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['service_request']),
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.service_request.request_number} - {self.rating} stars"