"""
Accounts views for the Farjad ERP system.

This module contains views for user management, authentication, and profiles.
"""

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    PasswordResetToken,
    Profile,
    Role,
    RolePermission,
    User,
    UserRole,
    UserSession,
)
from .serializers import (
    PermissionSerializer,
    ProfileSerializer,
    RegisterSerializer,
    RoleSerializer,
    UserProfileSerializer,
    UserRoleSerializer,
    UserSerializer,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user information."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["is_verified"] = user.is_verified

        return token


class LoginView(TokenObtainPairView):
    """Custom login view with enhanced token response."""

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User login",
        description="Authenticate user and return JWT tokens",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access": {"type": "string"},
                    "refresh": {"type": "string"},
                    "user": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "username": {"type": "string"},
                            "email": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "is_verified": {"type": "boolean"},
                        },
                    },
                },
            }
        },
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get user information - use email since USERNAME_FIELD is email
            email = request.data.get("email") or request.data.get("username")
            user = User.objects.get(email=email)
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_verified": user.is_verified,
            }

            # Add user data to response
            response.data["user"] = user_data

            # Create user session with unique session key
            import uuid

            session_key = request.session.session_key or str(uuid.uuid4())
            UserSession.objects.create(
                user=user,
                session_key=session_key,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )

        return response

    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


@extend_schema_view(
    list=extend_schema(
        summary="List users", description="Retrieve a list of all users"
    ),
    create=extend_schema(summary="Create user", description="Create a new user"),
    retrieve=extend_schema(summary="Get user", description="Retrieve a specific user"),
    update=extend_schema(summary="Update user", description="Update a specific user"),
    partial_update=extend_schema(
        summary="Partially update user", description="Partially update a specific user"
    ),
    destroy=extend_schema(summary="Delete user", description="Delete a specific user"),
)
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active", "is_verified"]
    search_fields = ["first_name", "last_name", "email", "username"]
    ordering_fields = ["first_name", "last_name", "date_joined"]
    ordering = ["last_name", "first_name"]


@extend_schema_view(
    list=extend_schema(
        summary="List profiles", description="Retrieve a list of all profiles"
    ),
    create=extend_schema(summary="Create profile", description="Create a new profile"),
    retrieve=extend_schema(
        summary="Get profile", description="Retrieve a specific profile"
    ),
    update=extend_schema(
        summary="Update profile", description="Update a specific profile"
    ),
    partial_update=extend_schema(
        summary="Partially update profile",
        description="Partially update a specific profile",
    ),
    destroy=extend_schema(
        summary="Delete profile", description="Delete a specific profile"
    ),
)
class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user profiles."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@extend_schema_view(
    list=extend_schema(
        summary="List roles", description="Retrieve a list of all roles"
    ),
    create=extend_schema(summary="Create role", description="Create a new role"),
    retrieve=extend_schema(summary="Get role", description="Retrieve a specific role"),
    update=extend_schema(summary="Update role", description="Update a specific role"),
    partial_update=extend_schema(
        summary="Partially update role", description="Partially update a specific role"
    ),
    destroy=extend_schema(summary="Delete role", description="Delete a specific role"),
)
class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing roles."""

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


@extend_schema_view(
    list=extend_schema(
        summary="List permissions", description="Retrieve a list of all permissions"
    ),
    retrieve=extend_schema(
        summary="Get permission", description="Retrieve a specific permission"
    ),
)
class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing permissions."""

    queryset = RolePermission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role", "granted"]
    search_fields = ["permission__name", "permission__content_type__model"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class RegisterView(generics.CreateAPIView):
    """User registration view."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(summary="Register user", description="Register a new user account")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view for current user."""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(summary="Get user profile", description="Get current user's profile")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update user profile", description="Update current user's profile"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Update user profile", description="Update current user's profile"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
