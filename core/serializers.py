"""
Core serializers for the Farjad ERP system.

This module contains serializers for core functionality including contacts, companies, and addresses.
"""

from rest_framework import serializers
from .models import Contact, Company, Address, SystemConfiguration, AuditLog


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Contact
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'mobile',
            'contact_type',
            'is_active',
            'notes',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company model."""
    
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'legal_name',
            'company_type',
            'tax_id',
            'registration_number',
            'website',
            'email',
            'phone',
            'fax',
            'is_active',
            'notes',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model."""
    
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Address
        fields = [
            'id',
            'contact',
            'contact_name',
            'company',
            'company_name',
            'address_type',
            'street_address',
            'city',
            'state',
            'postal_code',
            'country',
            'is_primary',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate that either contact or company is provided, but not both."""
        contact = data.get('contact')
        company = data.get('company')
        
        if not contact and not company:
            raise serializers.ValidationError('Either contact or company must be specified.')
        
        if contact and company:
            raise serializers.ValidationError('Cannot specify both contact and company.')
        
        return data


class SystemConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for SystemConfiguration model."""
    
    class Meta:
        model = SystemConfiguration
        fields = [
            'id',
            'key',
            'value',
            'description',
            'is_active',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model."""
    
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'user',
            'user_name',
            'action',
            'model_name',
            'object_id',
            'object_repr',
            'changes',
            'ip_address',
            'user_agent',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
