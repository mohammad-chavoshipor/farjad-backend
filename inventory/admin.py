"""
Inventory admin configuration for the Farjad ERP system.

This module contains admin configurations for product, category, brand, and inventory management.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Brand, Supplier, InventoryItem, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    
    list_display = [
        'name',
        'parent',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'parent',
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
        ('Category Information', {
            'fields': ('name', 'description', 'parent', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin configuration for Brand model."""
    
    list_display = [
        'name',
        'website',
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
        'website',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['name']
    
    fieldsets = (
        ('Brand Information', {
            'fields': ('name', 'description', 'website', 'logo', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Admin configuration for Supplier model."""
    
    list_display = [
        'name',
        'contact_person',
        'email',
        'city',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'city',
        'country',
        'created_at',
    ]
    search_fields = [
        'name',
        'contact_person',
        'email',
        'city',
        'tax_id',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'contact_person', 'email', 'phone')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'country')
        }),
        ('Business Information', {
            'fields': ('tax_id', 'payment_terms')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    
    list_display = [
        'name',
        'sku',
        'category',
        'brand',
        'selling_price',
        'current_stock',
        'status',
        'is_taxable',
    ]
    list_filter = [
        'status',
        'is_taxable',
        'category',
        'brand',
        'unit_type',
        'created_at',
    ]
    search_fields = [
        'name',
        'sku',
        'barcode',
        'description',
    ]
    readonly_fields = [
        'current_stock',
        'is_low_stock',
        'is_out_of_stock',
        'profit_margin',
        'created_at',
        'updated_at',
    ]
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'sku', 'barcode', 'description', 'short_description')
        }),
        ('Classification', {
            'fields': ('category', 'brand', 'status')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price', 'is_taxable', 'tax_rate')
        }),
        ('Inventory', {
            'fields': ('unit_type', 'min_stock_level', 'max_stock_level', 'current_stock', 'is_low_stock', 'is_out_of_stock')
        }),
        ('Physical Properties', {
            'fields': ('weight', 'dimensions')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Calculated Fields', {
            'fields': ('profit_margin',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    """Admin configuration for InventoryItem model."""
    
    list_display = [
        'product',
        'quantity',
        'transaction_type',
        'reference_number',
        'created_at',
        'created_by',
    ]
    list_filter = [
        'transaction_type',
        'created_at',
    ]
    search_fields = [
        'product__name',
        'product__sku',
        'reference_number',
        'notes',
    ]
    readonly_fields = [
        'created_at',
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('product', 'quantity', 'transaction_type', 'reference_number')
        }),
        ('Pricing', {
            'fields': ('unit_cost',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin configuration for ProductImage model."""
    
    list_display = [
        'product',
        'is_primary',
        'sort_order',
        'created_at',
    ]
    list_filter = [
        'is_primary',
        'created_at',
    ]
    search_fields = [
        'product__name',
        'product__sku',
        'alt_text',
    ]
    readonly_fields = [
        'created_at',
    ]
    ordering = ['product__name', 'sort_order']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('product', 'image', 'alt_text', 'is_primary', 'sort_order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )