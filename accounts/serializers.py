"""
Accounts serializers for the Farjad ERP system.

This module contains serializers for user management, authentication, and profiles.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    PasswordResetToken,
    Profile,
    Role,
    RolePermission,
    UserRole,
    UserSession,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "is_active",
            "is_verified",
            "date_joined",
            "last_login",
            "last_login_ip",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "avatar",
            "gender",
            "date_of_birth",
            "bio",
            "address",
            "city",
            "country",
            "postal_code",
            "emergency_contact_name",
            "emergency_contact_phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model."""

    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for RolePermission model."""

    role_name = serializers.CharField(source="role.name", read_only=True)
    permission_name = serializers.CharField(source="permission.name", read_only=True)
    permission_codename = serializers.CharField(
        source="permission.codename", read_only=True
    )
    content_type = serializers.CharField(
        source="permission.content_type.model", read_only=True
    )

    class Meta:
        model = RolePermission
        fields = [
            "id",
            "role",
            "role_name",
            "permission",
            "permission_name",
            "permission_codename",
            "content_type",
            "granted",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for UserRole model."""

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    role_name = serializers.CharField(source="role.name", read_only=True)
    assigned_by_name = serializers.CharField(
        source="assigned_by.full_name", read_only=True
    )

    class Meta:
        model = UserRole
        fields = [
            "id",
            "user",
            "user_name",
            "role",
            "role_name",
            "assigned_at",
            "assigned_by",
            "assigned_by_name",
            "is_active",
        ]
        read_only_fields = ["id", "assigned_at"]


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "password_confirm",
        ]

    def validate(self, data):
        """Validate password confirmation."""
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match.")
        return data

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile update."""

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile",
        ]
        read_only_fields = ["id", "username"]
