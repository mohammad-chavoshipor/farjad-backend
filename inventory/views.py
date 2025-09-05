"""
Inventory views for the Farjad ERP system.

This module contains views for product, category, brand, and inventory management.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Product, Category, Brand, Supplier, InventoryItem, ProductImage
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    BrandSerializer,
    SupplierSerializer,
    InventoryItemSerializer,
    ProductImageSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="List products", description="Retrieve a list of all products"),
    create=extend_schema(summary="Create product", description="Create a new product"),
    retrieve=extend_schema(summary="Get product", description="Retrieve a specific product"),
    update=extend_schema(summary="Update product", description="Update a specific product"),
    partial_update=extend_schema(summary="Partially update product", description="Partially update a specific product"),
    destroy=extend_schema(summary="Delete product", description="Delete a specific product"),
)
class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for managing products."""
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'brand', 'status', 'is_taxable']
    search_fields = ['name', 'sku', 'barcode', 'description']
    ordering_fields = ['name', 'sku', 'created_at', 'selling_price']
    ordering = ['name']


@extend_schema_view(
    list=extend_schema(summary="List categories", description="Retrieve a list of all categories"),
    create=extend_schema(summary="Create category", description="Create a new category"),
    retrieve=extend_schema(summary="Get category", description="Retrieve a specific category"),
    update=extend_schema(summary="Update category", description="Update a specific category"),
    partial_update=extend_schema(summary="Partially update category", description="Partially update a specific category"),
    destroy=extend_schema(summary="Delete category", description="Delete a specific category"),
)
class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing categories."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


@extend_schema_view(
    list=extend_schema(summary="List brands", description="Retrieve a list of all brands"),
    create=extend_schema(summary="Create brand", description="Create a new brand"),
    retrieve=extend_schema(summary="Get brand", description="Retrieve a specific brand"),
    update=extend_schema(summary="Update brand", description="Update a specific brand"),
    partial_update=extend_schema(summary="Partially update brand", description="Partially update a specific brand"),
    destroy=extend_schema(summary="Delete brand", description="Delete a specific brand"),
)
class BrandViewSet(viewsets.ModelViewSet):
    """ViewSet for managing brands."""
    
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


@extend_schema_view(
    list=extend_schema(summary="List suppliers", description="Retrieve a list of all suppliers"),
    create=extend_schema(summary="Create supplier", description="Create a new supplier"),
    retrieve=extend_schema(summary="Get supplier", description="Retrieve a specific supplier"),
    update=extend_schema(summary="Update supplier", description="Update a specific supplier"),
    partial_update=extend_schema(summary="Partially update supplier", description="Partially update a specific supplier"),
    destroy=extend_schema(summary="Delete supplier", description="Delete a specific supplier"),
)
class SupplierViewSet(viewsets.ModelViewSet):
    """ViewSet for managing suppliers."""
    
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'contact_person', 'email', 'city']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


@extend_schema_view(
    list=extend_schema(summary="List inventory items", description="Retrieve a list of all inventory items"),
    create=extend_schema(summary="Create inventory item", description="Create a new inventory item"),
    retrieve=extend_schema(summary="Get inventory item", description="Retrieve a specific inventory item"),
    update=extend_schema(summary="Update inventory item", description="Update a specific inventory item"),
    partial_update=extend_schema(summary="Partially update inventory item", description="Partially update a specific inventory item"),
    destroy=extend_schema(summary="Delete inventory item", description="Delete a specific inventory item"),
)
class InventoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing inventory items."""
    
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'transaction_type']
    search_fields = ['product__name', 'reference_number', 'notes']
    ordering_fields = ['created_at', 'quantity']
    ordering = ['-created_at']