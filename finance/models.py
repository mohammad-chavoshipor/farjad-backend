"""
Finance models for the Farjad ERP system.

This module contains invoice, payment, and financial transaction models.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

User = get_user_model()


class Account(models.Model):
    """Chart of accounts model."""
    
    ACCOUNT_TYPES = [
        ('asset', _('Asset')),
        ('liability', _('Liability')),
        ('equity', _('Equity')),
        ('revenue', _('Revenue')),
        ('expense', _('Expense')),
    ]
    
    name = models.CharField(_('Name'), max_length=200)
    code = models.CharField(_('Account code'), max_length=20, unique=True)
    account_type = models.CharField(_('Account type'), max_length=20, choices=ACCOUNT_TYPES)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent account')
    )
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['account_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Invoice(models.Model):
    """Invoice model for billing customers."""
    
    INVOICE_TYPES = [
        ('sale', _('Sale')),
        ('service', _('Service')),
        ('credit', _('Credit Note')),
        ('debit', _('Debit Note')),
    ]
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('paid', _('Paid')),
        ('overdue', _('Overdue')),
        ('cancelled', _('Cancelled')),
    ]
    
    # Basic Information
    invoice_number = models.CharField(_('Invoice number'), max_length=50, unique=True)
    invoice_type = models.CharField(_('Invoice type'), max_length=20, choices=INVOICE_TYPES, default='sale')
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Customer Information
    customer = models.ForeignKey(
        'core.Contact',
        on_delete=models.PROTECT,
        related_name='invoices',
        verbose_name=_('Customer')
    )
    customer_company = models.ForeignKey(
        'core.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices',
        verbose_name=_('Customer company')
    )
    
    # Dates
    invoice_date = models.DateField(_('Invoice date'))
    due_date = models.DateField(_('Due date'))
    sent_date = models.DateTimeField(_('Sent date'), null=True, blank=True)
    paid_date = models.DateTimeField(_('Paid date'), null=True, blank=True)
    
    # Amounts
    subtotal = models.DecimalField(
        _('Subtotal'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    tax_amount = models.DecimalField(
        _('Tax amount'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    discount_amount = models.DecimalField(
        _('Discount amount'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    total_amount = models.DecimalField(
        _('Total amount'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Tax Information
    tax_rate = models.DecimalField(
        _('Tax rate'),
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    
    # Notes and Terms
    notes = models.TextField(_('Notes'), blank=True)
    terms_and_conditions = models.TextField(_('Terms and conditions'), blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_invoices',
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-invoice_date', '-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['invoice_date']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.invoice_number} - {self.customer.full_name}"

    def save(self, *args, **kwargs):
        """Generate invoice number if not provided."""
        if not self.invoice_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.invoice_number = f"INV-{timestamp}"
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Check if invoice is overdue."""
        from django.utils import timezone
        return self.status not in ['paid', 'cancelled'] and timezone.now().date() > self.due_date

    @property
    def remaining_amount(self):
        """Calculate remaining amount to be paid."""
        total_paid = self.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
        return self.total_amount - total_paid


class InvoiceItem(models.Model):
    """Invoice item model for line items."""
    
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Invoice')
    )
    description = models.CharField(_('Description'), max_length=500)
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unit_price = models.DecimalField(
        _('Unit price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    discount_percentage = models.DecimalField(
        _('Discount percentage'),
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    line_total = models.DecimalField(
        _('Line total'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    class Meta:
        verbose_name = _('Invoice Item')
        verbose_name_plural = _('Invoice Items')
        ordering = ['id']
        indexes = [
            models.Index(fields=['invoice']),
        ]

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description}"

    def save(self, *args, **kwargs):
        """Calculate line total before saving."""
        discount_amount = (self.unit_price * self.quantity * self.discount_percentage) / 100
        self.line_total = (self.unit_price * self.quantity) - discount_amount
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Payment model for tracking payments."""
    
    PAYMENT_METHODS = [
        ('cash', _('Cash')),
        ('check', _('Check')),
        ('bank_transfer', _('Bank Transfer')),
        ('credit_card', _('Credit Card')),
        ('online', _('Online Payment')),
        ('other', _('Other')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]
    
    # Basic Information
    payment_number = models.CharField(_('Payment number'), max_length=50, unique=True)
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('Invoice')
    )
    amount = models.DecimalField(
        _('Amount'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_method = models.CharField(_('Payment method'), max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment Details
    payment_date = models.DateTimeField(_('Payment date'))
    reference_number = models.CharField(_('Reference number'), max_length=100, blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    
    # Bank Information (for bank transfers)
    bank_name = models.CharField(_('Bank name'), max_length=100, blank=True)
    account_number = models.CharField(_('Account number'), max_length=50, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_payments',
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['payment_number']),
            models.Index(fields=['invoice']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_date']),
        ]

    def __str__(self):
        return f"{self.payment_number} - {self.amount}"

    def save(self, *args, **kwargs):
        """Generate payment number if not provided."""
        if not self.payment_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.payment_number = f"PAY-{timestamp}"
        super().save(*args, **kwargs)


class Transaction(models.Model):
    """General transaction model for accounting."""
    
    TRANSACTION_TYPES = [
        ('debit', _('Debit')),
        ('credit', _('Credit')),
    ]
    
    # Basic Information
    transaction_number = models.CharField(_('Transaction number'), max_length=50, unique=True)
    description = models.CharField(_('Description'), max_length=500)
    transaction_date = models.DateField(_('Transaction date'))
    amount = models.DecimalField(
        _('Amount'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Account Information
    debit_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='debit_transactions',
        verbose_name=_('Debit account')
    )
    credit_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='credit_transactions',
        verbose_name=_('Credit account')
    )
    
    # Reference Information
    reference_type = models.CharField(_('Reference type'), max_length=50, blank=True)
    reference_id = models.CharField(_('Reference ID'), max_length=50, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['transaction_number']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['debit_account']),
            models.Index(fields=['credit_account']),
        ]

    def __str__(self):
        return f"{self.transaction_number} - {self.description}"

    def save(self, *args, **kwargs):
        """Generate transaction number if not provided."""
        if not self.transaction_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.transaction_number = f"TXN-{timestamp}"
        super().save(*args, **kwargs)


class Expense(models.Model):
    """Expense model for tracking business expenses."""
    
    EXPENSE_CATEGORIES = [
        ('office', _('Office Supplies')),
        ('travel', _('Travel')),
        ('utilities', _('Utilities')),
        ('marketing', _('Marketing')),
        ('maintenance', _('Maintenance')),
        ('other', _('Other')),
    ]
    
    # Basic Information
    expense_number = models.CharField(_('Expense number'), max_length=50, unique=True)
    description = models.CharField(_('Description'), max_length=500)
    category = models.CharField(_('Category'), max_length=20, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(
        _('Amount'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    expense_date = models.DateField(_('Expense date'))
    
    # Account Information
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='expenses',
        verbose_name=_('Account')
    )
    
    # Vendor Information
    vendor = models.ForeignKey(
        'core.Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
        verbose_name=_('Vendor')
    )
    
    # Receipt Information
    receipt_number = models.CharField(_('Receipt number'), max_length=100, blank=True)
    receipt_image = models.ImageField(_('Receipt image'), upload_to='receipts/', blank=True, null=True)
    
    # Approval
    is_approved = models.BooleanField(_('Is approved'), default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_expenses',
        verbose_name=_('Approved by')
    )
    approved_at = models.DateTimeField(_('Approved at'), null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_expenses',
        verbose_name=_('Created by')
    )

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
        ordering = ['-expense_date']
        indexes = [
            models.Index(fields=['expense_number']),
            models.Index(fields=['category']),
            models.Index(fields=['expense_date']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        return f"{self.expense_number} - {self.description}"

    def save(self, *args, **kwargs):
        """Generate expense number if not provided."""
        if not self.expense_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.expense_number = f"EXP-{timestamp}"
        super().save(*args, **kwargs)