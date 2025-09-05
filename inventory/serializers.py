"""
Inventory serializers for the Farjad ERP system.

This module contains serializers for product, category, brand, and inventory management.
"""

from rest_framework import serializers
from .models import Product, Category, Brand, Supplier, InventoryItem, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    full_path = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'parent',
            'full_path',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand model."""
    
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description',
            'website',
            'logo',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model."""
    
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'contact_person',
            'email',
            'phone',
            'address',
            'city',
            'country',
            'tax_id',
            'payment_terms',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    
    current_stock = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    is_out_of_stock = serializers.ReadOnlyField()
    profit_margin = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'barcode',
            'description',
            'short_description',
            'category',
            'category_name',
            'brand',
            'brand_name',
            'cost_price',
            'selling_price',
            'unit_type',
            'min_stock_level',
            'max_stock_level',
            'weight',
            'dimensions',
            'status',
            'is_taxable',
            'tax_rate',
            'image',
            'current_stock',
            'is_low_stock',
            'is_out_of_stock',
            'profit_margin',
            'created_at',
            'updated_at',
            'created_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage model."""
    
    class Meta:
        model = ProductImage
        fields = [
            'id',
            'product',
            'image',
            'alt_text',
            'is_primary',
            'sort_order',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for InventoryItem model."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_sku',
            'quantity',
            'transaction_type',
            'reference_number',
            'notes',
            'unit_cost',
            'created_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'created_at']
