"""
Core views for the Farjad ERP system.

This module contains views for core functionality including contacts, companies, and addresses.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Contact, Company, Address, SystemConfiguration, AuditLog
from .serializers import (
    ContactSerializer,
    CompanySerializer,
    AddressSerializer,
    SystemConfigurationSerializer,
    AuditLogSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="List contacts", description="Retrieve a list of all contacts"),
    create=extend_schema(summary="Create contact", description="Create a new contact"),
    retrieve=extend_schema(summary="Get contact", description="Retrieve a specific contact"),
    update=extend_schema(summary="Update contact", description="Update a specific contact"),
    partial_update=extend_schema(summary="Partially update contact", description="Partially update a specific contact"),
    destroy=extend_schema(summary="Delete contact", description="Delete a specific contact"),
)
class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet for managing contacts."""
    
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['contact_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    ordering = ['last_name', 'first_name']

    @extend_schema(summary="Get contact statistics", description="Get statistics for contacts")
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get contact statistics."""
        stats = {
            'total_contacts': Contact.objects.count(),
            'active_contacts': Contact.objects.filter(is_active=True).count(),
            'inactive_contacts': Contact.objects.filter(is_active=False).count(),
            'by_type': {
                contact_type: Contact.objects.filter(contact_type=contact_type).count()
                for contact_type, _ in Contact.CONTACT_TYPES
            }
        }
        return Response(stats)


@extend_schema_view(
    list=extend_schema(summary="List companies", description="Retrieve a list of all companies"),
    create=extend_schema(summary="Create company", description="Create a new company"),
    retrieve=extend_schema(summary="Get company", description="Retrieve a specific company"),
    update=extend_schema(summary="Update company", description="Update a specific company"),
    partial_update=extend_schema(summary="Partially update company", description="Partially update a specific company"),
    destroy=extend_schema(summary="Delete company", description="Delete a specific company"),
)
class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for managing companies."""
    
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company_type', 'is_active']
    search_fields = ['name', 'legal_name', 'email', 'tax_id']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @extend_schema(summary="Get company statistics", description="Get statistics for companies")
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get company statistics."""
        stats = {
            'total_companies': Company.objects.count(),
            'active_companies': Company.objects.filter(is_active=True).count(),
            'inactive_companies': Company.objects.filter(is_active=False).count(),
            'by_type': {
                company_type: Company.objects.filter(company_type=company_type).count()
                for company_type, _ in Company.COMPANY_TYPES
            }
        }
        return Response(stats)


@extend_schema_view(
    list=extend_schema(summary="List addresses", description="Retrieve a list of all addresses"),
    create=extend_schema(summary="Create address", description="Create a new address"),
    retrieve=extend_schema(summary="Get address", description="Retrieve a specific address"),
    update=extend_schema(summary="Update address", description="Update a specific address"),
    partial_update=extend_schema(summary="Partially update address", description="Partially update a specific address"),
    destroy=extend_schema(summary="Delete address", description="Delete a specific address"),
)
class AddressViewSet(viewsets.ModelViewSet):
    """ViewSet for managing addresses."""
    
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['address_type', 'is_primary', 'contact', 'company']
    search_fields = ['street_address', 'city', 'state', 'postal_code']
    ordering_fields = ['city', 'created_at']
    ordering = ['city', 'street_address']


@extend_schema_view(
    list=extend_schema(summary="List system configurations", description="Retrieve a list of all system configurations"),
    create=extend_schema(summary="Create system configuration", description="Create a new system configuration"),
    retrieve=extend_schema(summary="Get system configuration", description="Retrieve a specific system configuration"),
    update=extend_schema(summary="Update system configuration", description="Update a specific system configuration"),
    partial_update=extend_schema(summary="Partially update system configuration", description="Partially update a specific system configuration"),
    destroy=extend_schema(summary="Delete system configuration", description="Delete a specific system configuration"),
)
class SystemConfigurationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing system configurations."""
    
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['key', 'description']
    ordering_fields = ['key', 'created_at']
    ordering = ['key']


@extend_schema_view(
    list=extend_schema(summary="List audit logs", description="Retrieve a list of all audit logs"),
    retrieve=extend_schema(summary="Get audit log", description="Retrieve a specific audit log"),
)
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing audit logs."""
    
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['action', 'model_name', 'user']
    search_fields = ['object_repr', 'ip_address']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


def health_check(request):
    """Health check endpoint."""
    return Response({
        'status': 'healthy',
        'message': 'Farjad ERP API is running',
        'version': '1.0.0'
    })