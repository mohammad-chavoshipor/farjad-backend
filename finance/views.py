"""
Finance views for the Farjad ERP system.

This module contains views for invoice, payment, and financial transaction management.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Account, Invoice, InvoiceItem, Payment, Transaction, Expense
from .serializers import (
    AccountSerializer,
    InvoiceSerializer,
    InvoiceItemSerializer,
    PaymentSerializer,
    TransactionSerializer,
    ExpenseSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="List accounts", description="Retrieve a list of all accounts"),
    create=extend_schema(summary="Create account", description="Create a new account"),
    retrieve=extend_schema(summary="Get account", description="Retrieve a specific account"),
    update=extend_schema(summary="Update account", description="Update a specific account"),
    partial_update=extend_schema(summary="Partially update account", description="Partially update a specific account"),
    destroy=extend_schema(summary="Delete account", description="Delete a specific account"),
)
class AccountViewSet(viewsets.ModelViewSet):
    """ViewSet for managing accounts."""
    
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['account_type', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['code', 'name', 'created_at']
    ordering = ['code']


@extend_schema_view(
    list=extend_schema(summary="List invoices", description="Retrieve a list of all invoices"),
    create=extend_schema(summary="Create invoice", description="Create a new invoice"),
    retrieve=extend_schema(summary="Get invoice", description="Retrieve a specific invoice"),
    update=extend_schema(summary="Update invoice", description="Update a specific invoice"),
    partial_update=extend_schema(summary="Partially update invoice", description="Partially update a specific invoice"),
    destroy=extend_schema(summary="Delete invoice", description="Delete a specific invoice"),
)
class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing invoices."""
    
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'invoice_type', 'customer']
    search_fields = ['invoice_number', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['invoice_date', 'due_date', 'total_amount', 'created_at']
    ordering = ['-invoice_date']


@extend_schema_view(
    list=extend_schema(summary="List payments", description="Retrieve a list of all payments"),
    create=extend_schema(summary="Create payment", description="Create a new payment"),
    retrieve=extend_schema(summary="Get payment", description="Retrieve a specific payment"),
    update=extend_schema(summary="Update payment", description="Update a specific payment"),
    partial_update=extend_schema(summary="Partially update payment", description="Partially update a specific payment"),
    destroy=extend_schema(summary="Delete payment", description="Delete a specific payment"),
)
class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing payments."""
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'invoice']
    search_fields = ['payment_number', 'reference_number', 'notes']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    ordering = ['-payment_date']


@extend_schema_view(
    list=extend_schema(summary="List transactions", description="Retrieve a list of all transactions"),
    create=extend_schema(summary="Create transaction", description="Create a new transaction"),
    retrieve=extend_schema(summary="Get transaction", description="Retrieve a specific transaction"),
    update=extend_schema(summary="Update transaction", description="Update a specific transaction"),
    partial_update=extend_schema(summary="Partially update transaction", description="Partially update a specific transaction"),
    destroy=extend_schema(summary="Delete transaction", description="Delete a specific transaction"),
)
class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transactions."""
    
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['debit_account', 'credit_account']
    search_fields = ['transaction_number', 'description', 'reference_type']
    ordering_fields = ['transaction_date', 'amount', 'created_at']
    ordering = ['-transaction_date']