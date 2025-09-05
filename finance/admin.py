"""
Finance admin configuration for the Farjad ERP system.

This module contains admin configurations for invoice, payment, and financial transaction management.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Account, Invoice, InvoiceItem, Payment, Transaction, Expense


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Admin configuration for Account model."""
    
    list_display = [
        'code',
        'name',
        'account_type',
        'parent',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'account_type',
        'is_active',
        'parent',
        'created_at',
    ]
    search_fields = [
        'name',
        'code',
        'description',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['code']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('name', 'code', 'account_type', 'parent', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Admin configuration for Invoice model."""
    
    list_display = [
        'invoice_number',
        'customer',
        'invoice_type',
        'status',
        'total_amount',
        'invoice_date',
        'due_date',
        'is_overdue',
    ]
    list_filter = [
        'status',
        'invoice_type',
        'invoice_date',
        'due_date',
        'created_at',
    ]
    search_fields = [
        'invoice_number',
        'customer__first_name',
        'customer__last_name',
        'customer__email',
    ]
    readonly_fields = [
        'invoice_number',
        'is_overdue',
        'remaining_amount',
        'created_at',
        'updated_at',
    ]
    ordering = ['-invoice_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('invoice_number', 'invoice_type', 'status')
        }),
        ('Customer Information', {
            'fields': ('customer', 'customer_company')
        }),
        ('Dates', {
            'fields': ('invoice_date', 'due_date', 'sent_date', 'paid_date')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'tax_rate')
        }),
        ('Calculated Fields', {
            'fields': ('is_overdue', 'remaining_amount'),
            'classes': ('collapse',)
        }),
        ('Terms and Notes', {
            'fields': ('notes', 'terms_and_conditions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    """Admin configuration for InvoiceItem model."""
    
    list_display = [
        'invoice',
        'description',
        'quantity',
        'unit_price',
        'line_total',
    ]
    list_filter = [
        'invoice__status',
        'invoice__invoice_type',
    ]
    search_fields = [
        'invoice__invoice_number',
        'description',
    ]
    ordering = ['invoice', 'id']
    
    fieldsets = (
        ('Item Information', {
            'fields': ('invoice', 'description', 'quantity', 'unit_price', 'discount_percentage', 'line_total')
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for Payment model."""
    
    list_display = [
        'payment_number',
        'invoice',
        'amount',
        'payment_method',
        'status',
        'payment_date',
        'created_at',
    ]
    list_filter = [
        'status',
        'payment_method',
        'payment_date',
        'created_at',
    ]
    search_fields = [
        'payment_number',
        'invoice__invoice_number',
        'reference_number',
        'notes',
    ]
    readonly_fields = [
        'payment_number',
        'created_at',
        'updated_at',
    ]
    ordering = ['-payment_date']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_number', 'invoice', 'amount', 'payment_method', 'status')
        }),
        ('Payment Details', {
            'fields': ('payment_date', 'reference_number', 'notes')
        }),
        ('Bank Information', {
            'fields': ('bank_name', 'account_number'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model."""
    
    list_display = [
        'transaction_number',
        'description',
        'amount',
        'debit_account',
        'credit_account',
        'transaction_date',
        'created_at',
    ]
    list_filter = [
        'transaction_date',
        'debit_account__account_type',
        'credit_account__account_type',
        'created_at',
    ]
    search_fields = [
        'transaction_number',
        'description',
        'reference_type',
        'reference_id',
    ]
    readonly_fields = [
        'transaction_number',
        'created_at',
    ]
    ordering = ['-transaction_date']
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_number', 'description', 'transaction_date', 'amount')
        }),
        ('Account Information', {
            'fields': ('debit_account', 'credit_account')
        }),
        ('Reference Information', {
            'fields': ('reference_type', 'reference_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Admin configuration for Expense model."""
    
    list_display = [
        'expense_number',
        'description',
        'category',
        'amount',
        'expense_date',
        'is_approved',
        'created_at',
    ]
    list_filter = [
        'category',
        'is_approved',
        'expense_date',
        'created_at',
    ]
    search_fields = [
        'expense_number',
        'description',
        'vendor__first_name',
        'vendor__last_name',
        'receipt_number',
    ]
    readonly_fields = [
        'expense_number',
        'created_at',
    ]
    ordering = ['-expense_date']
    
    fieldsets = (
        ('Expense Information', {
            'fields': ('expense_number', 'description', 'category', 'amount', 'expense_date')
        }),
        ('Account and Vendor', {
            'fields': ('account', 'vendor')
        }),
        ('Receipt Information', {
            'fields': ('receipt_number', 'receipt_image')
        }),
        ('Approval', {
            'fields': ('is_approved', 'approved_by', 'approved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )