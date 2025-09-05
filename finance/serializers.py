"""
Finance serializers for the Farjad ERP system.

This module contains serializers for invoice, payment, and financial transaction management.
"""

from rest_framework import serializers
from .models import Account, Invoice, InvoiceItem, Payment, Transaction, Expense


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account model."""
    
    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'code',
            'account_type',
            'parent',
            'description',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvoiceItemSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceItem model."""
    
    class Meta:
        model = InvoiceItem
        fields = [
            'id',
            'invoice',
            'description',
            'quantity',
            'unit_price',
            'discount_percentage',
            'line_total',
        ]
        read_only_fields = ['id']


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model."""
    
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    customer_company_name = serializers.CharField(source='customer_company.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    items = InvoiceItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'invoice_type',
            'status',
            'customer',
            'customer_name',
            'customer_company',
            'customer_company_name',
            'invoice_date',
            'due_date',
            'sent_date',
            'paid_date',
            'subtotal',
            'tax_amount',
            'discount_amount',
            'total_amount',
            'tax_rate',
            'notes',
            'terms_and_conditions',
            'is_overdue',
            'remaining_amount',
            'items',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'invoice_number', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'payment_number',
            'invoice',
            'invoice_number',
            'amount',
            'payment_method',
            'status',
            'payment_date',
            'reference_number',
            'notes',
            'bank_name',
            'account_number',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'payment_number', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""
    
    debit_account_name = serializers.CharField(source='debit_account.name', read_only=True)
    credit_account_name = serializers.CharField(source='credit_account.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'transaction_number',
            'description',
            'transaction_date',
            'amount',
            'debit_account',
            'debit_account_name',
            'credit_account',
            'credit_account_name',
            'reference_type',
            'reference_id',
            'created_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'transaction_number', 'created_at']


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model."""
    
    account_name = serializers.CharField(source='account.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.full_name', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id',
            'expense_number',
            'description',
            'category',
            'amount',
            'expense_date',
            'account',
            'account_name',
            'vendor',
            'vendor_name',
            'receipt_number',
            'receipt_image',
            'is_approved',
            'approved_by',
            'approved_by_name',
            'approved_at',
            'created_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'expense_number', 'created_at']
