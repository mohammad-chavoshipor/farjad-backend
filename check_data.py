#!/usr/bin/env python
"""
Script to check database and create sample data if needed.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farjad.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from inventory.models import Product, Category, Brand, Supplier
from core.models import Contact, Company
from services.models import ServiceRequest, ServiceType
from finance.models import Invoice, Account

User = get_user_model()

def check_and_create_data():
    print("Checking database...")
    
    # Check users
    user_count = User.objects.count()
    print(f"Users: {user_count}")
    
    if user_count == 0:
        print("Creating admin user...")
        user = User.objects.create_user(
            username='admin',
            email='admin@farjad.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True
        )
        print(f"Created user: {user.email}")
    
    # Check categories
    category_count = Category.objects.count()
    print(f"Categories: {category_count}")
    
    if category_count == 0:
        print("Creating sample categories...")
        categories = [
            {'name': 'Electronics', 'description': 'Electronic products'},
            {'name': 'Tools', 'description': 'Industrial tools'},
            {'name': 'Parts', 'description': 'Spare parts'},
        ]
        for cat_data in categories:
            Category.objects.create(**cat_data)
        print("Created sample categories")
    
    # Check brands
    brand_count = Brand.objects.count()
    print(f"Brands: {brand_count}")
    
    if brand_count == 0:
        print("Creating sample brands...")
        brands = [
            {'name': 'Siemens', 'description': 'Siemens industrial equipment'},
            {'name': 'ABB', 'description': 'ABB automation products'},
            {'name': 'Schneider', 'description': 'Schneider Electric products'},
        ]
        for brand_data in brands:
            Brand.objects.create(**brand_data)
        print("Created sample brands")
    
    # Check suppliers
    supplier_count = Supplier.objects.count()
    print(f"Suppliers: {supplier_count}")
    
    if supplier_count == 0:
        print("Creating sample suppliers...")
        suppliers = [
            {
                'name': 'Industrial Supply Co.',
                'contact_person': 'John Smith',
                'email': 'john@industrialsupply.com',
                'phone': '+1-555-0123',
                'address': '123 Industrial Blvd, City, State 12345'
            },
            {
                'name': 'Tech Parts Ltd.',
                'contact_person': 'Jane Doe',
                'email': 'jane@techparts.com',
                'phone': '+1-555-0456',
                'address': '456 Technology Ave, City, State 12345'
            }
        ]
        for supplier_data in suppliers:
            Supplier.objects.create(**supplier_data)
        print("Created sample suppliers")
    
    # Check products
    product_count = Product.objects.count()
    print(f"Products: {product_count}")
    
    if product_count == 0:
        print("Creating sample products...")
        category = Category.objects.first()
        brand = Brand.objects.first()
        supplier = Supplier.objects.first()
        
        products = [
            {
                'name': 'Industrial Motor',
                'description': 'High-performance industrial motor',
                'sku': 'MOT-001',
                'price': 1500.00,
                'cost': 1200.00,
                'category': category,
                'brand': brand,
                'supplier': supplier,
                'is_active': True
            },
            {
                'name': 'Control Panel',
                'description': 'Advanced control panel system',
                'sku': 'CP-001',
                'price': 2500.00,
                'cost': 2000.00,
                'category': category,
                'brand': brand,
                'supplier': supplier,
                'is_active': True
            }
        ]
        for product_data in products:
            Product.objects.create(**product_data)
        print("Created sample products")
    
    # Check contacts
    contact_count = Contact.objects.count()
    print(f"Contacts: {contact_count}")
    
    if contact_count == 0:
        print("Creating sample contacts...")
        contacts = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'phone': '+1-555-0100',
                'position': 'Engineer',
                'is_active': True
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@example.com',
                'phone': '+1-555-0101',
                'position': 'Manager',
                'is_active': True
            }
        ]
        for contact_data in contacts:
            Contact.objects.create(**contact_data)
        print("Created sample contacts")
    
    # Check service types
    service_type_count = ServiceType.objects.count()
    print(f"Service Types: {service_type_count}")
    
    if service_type_count == 0:
        print("Creating sample service types...")
        service_types = [
            {
                'name': 'Maintenance',
                'description': 'Regular maintenance services',
                'base_price': 200.00,
                'estimated_duration': 120,
                'is_active': True
            },
            {
                'name': 'Repair',
                'description': 'Equipment repair services',
                'base_price': 300.00,
                'estimated_duration': 180,
                'is_active': True
            }
        ]
        for st_data in service_types:
            ServiceType.objects.create(**st_data)
        print("Created sample service types")
    
    # Check accounts
    account_count = Account.objects.count()
    print(f"Accounts: {account_count}")
    
    if account_count == 0:
        print("Creating sample accounts...")
        accounts = [
            {
                'name': 'Cash Account',
                'account_type': 'asset',
                'balance': 10000.00,
                'is_active': True
            },
            {
                'name': 'Sales Revenue',
                'account_type': 'revenue',
                'balance': 0.00,
                'is_active': True
            }
        ]
        for account_data in accounts:
            Account.objects.create(**account_data)
        print("Created sample accounts")
    
    print("\nDatabase check complete!")
    print(f"Users: {User.objects.count()}")
    print(f"Categories: {Category.objects.count()}")
    print(f"Brands: {Brand.objects.count()}")
    print(f"Suppliers: {Supplier.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Contacts: {Contact.objects.count()}")
    print(f"Service Types: {ServiceType.objects.count()}")
    print(f"Accounts: {Account.objects.count()}")

if __name__ == '__main__':
    check_and_create_data()
