"""
Inventory models for the Farjad ERP system.

This module contains product, category, brand, and inventory management models.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

User = get_user_model()


class Category(models.Model):
    """Product category model."""
    
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent category')
    )
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['parent']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

    @property
    def full_path(self):
        """Return the full category path."""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name


class Brand(models.Model):
    """Product brand model."""
    
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    website = models.URLField(_('Website'), blank=True)
    logo = models.ImageField(_('Logo'), upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Supplier model for product suppliers."""
    
    name = models.CharField(_('Name'), max_length=200)
    contact_person = models.CharField(_('Contact person'), max_length=100, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    address = models.TextField(_('Address'), blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    country = models.CharField(_('Country'), max_length=100, default='Iran')
    tax_id = models.CharField(_('Tax ID'), max_length=50, blank=True)
    payment_terms = models.CharField(_('Payment terms'), max_length=100, blank=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model for inventory management."""
    
    UNIT_TYPES = [
        ('piece', _('Piece')),
        ('kg', _('Kilogram')),
        ('gram', _('Gram')),
        ('liter', _('Liter')),
        ('meter', _('Meter')),
        ('box', _('Box')),
        ('pack', _('Pack')),
    ]
    
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('discontinued', _('Discontinued')),
    ]
    
    # Basic Information
    name = models.CharField(_('Name'), max_length=200)
    sku = models.CharField(_('SKU'), max_length=100, unique=True)
    barcode = models.CharField(_('Barcode'), max_length=100, blank=True, unique=True, null=True)
    description = models.TextField(_('Description'), blank=True)
    short_description = models.CharField(_('Short description'), max_length=500, blank=True)
    
    # Classification
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('Category')
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('Brand')
    )
    
    # Pricing
    cost_price = models.DecimalField(
        _('Cost price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    selling_price = models.DecimalField(
        _('Selling price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Inventory
    unit_type = models.CharField(_('Unit type'), max_length=20, choices=UNIT_TYPES, default='piece')
    min_stock_level = models.PositiveIntegerField(_('Minimum stock level'), default=0)
    max_stock_level = models.PositiveIntegerField(_('Maximum stock level'), default=1000)
    
    # Physical Properties
    weight = models.DecimalField(
        _('Weight'),
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.000'))]
    )
    dimensions = models.CharField(_('Dimensions'), max_length=100, blank=True)  # e.g., "10x20x30 cm"
    
    # Status and Metadata
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='active')
    is_taxable = models.BooleanField(_('Is taxable'), default=True)
    tax_rate = models.DecimalField(
        _('Tax rate'),
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    
    # Images
    image = models.ImageField(_('Image'), upload_to='products/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_products',
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['barcode']),
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0

    @property
    def current_stock(self):
        """Get current stock level."""
        return self.inventory_items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    @property
    def is_low_stock(self):
        """Check if product is low on stock."""
        return self.current_stock <= self.min_stock_level

    @property
    def is_out_of_stock(self):
        """Check if product is out of stock."""
        return self.current_stock <= 0


class InventoryItem(models.Model):
    """Inventory item model for tracking stock levels."""
    
    TRANSACTION_TYPES = [
        ('in', _('Stock In')),
        ('out', _('Stock Out')),
        ('adjustment', _('Adjustment')),
        ('transfer', _('Transfer')),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name=_('Product')
    )
    quantity = models.IntegerField(_('Quantity'))
    transaction_type = models.CharField(_('Transaction type'), max_length=20, choices=TRANSACTION_TYPES)
    reference_number = models.CharField(_('Reference number'), max_length=100, blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    unit_cost = models.DecimalField(
        _('Unit cost'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Inventory Item')
        verbose_name_plural = _('Inventory Items')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity} ({self.transaction_type})"


class ProductImage(models.Model):
    """Product image model for multiple product images."""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Product')
    )
    image = models.ImageField(_('Image'), upload_to='products/images/')
    alt_text = models.CharField(_('Alt text'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('Is primary'), default=False)
    sort_order = models.PositiveIntegerField(_('Sort order'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        ordering = ['sort_order', 'created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['is_primary']),
            models.Index(fields=['sort_order']),
        ]

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

    def clean(self):
        """Ensure only one primary image per product."""
        from django.core.exceptions import ValidationError
        
        if self.is_primary:
            existing_primary = ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(pk=self.pk)
            
            if existing_primary.exists():
                raise ValidationError(_('Only one primary image is allowed per product.'))