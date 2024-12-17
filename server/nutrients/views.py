from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Nutrient
from .serializers import NutrientSerializer
from common.permission_classes import IsAdminOrDietitian


class NutrientViewSet(ModelViewSet):
    """
    API endpoint for Nutrient table (add, edit, remove, list).
    """
    serializer_class = NutrientSerializer
    # Set permissions to API
    permission_classes = [IsAdminOrDietitian]

    # Filters and search
    filter_backends = [
        DjangoFilterBackend,  # Handle filter
        SearchFilter,         # Handle search
        OrderingFilter        # Handle sort
    ]

    # Filter
    filterset_fields = ['unit']  # User can filter by 'unit' field

    # Search
    search_fields = ['name']  # User can search by `name` field

    # Sort
    ordering_fields = ['name', 'unit']  # User can order by 'unit' or 'name' fields

    def get_queryset(self):
        user = self.request.user

        # Admin sees all objects
        if user.role == 'admin':
            return Nutrient.objects.all()

        # Dietitian sees only public meals or their own meals
        if user.role == 'dietitian':
            return Nutrient.objects.filter(
                Q(author=user) | Q(visibility='public')
            )

        # In other cases, no access
        return Nutrient.objects.none()

    def perform_update(self, instance):
        # Check if the user has permission to edit the object
        obj = self.get_object()
        if obj.author != self.request.user and self.request.user.role != 'admin':
            raise PermissionDenied("You don't have permission to edit this object.")
        instance.save()

    def perform_destroy(self, instance):
        # Check if the user has permission to delete the object
        obj = self.get_object()
        if obj.author != self.request.user and self.request.user.role != 'admin':
            raise PermissionDenied("You don't have permission to delete this object.")
        instance.delete()

    def perform_create(self, instance):
        # Add author to the object
        instance.save(author=self.request.user)

