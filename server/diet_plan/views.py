from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import DietPlan
from .serializers import DietPlanSerializer
from common.permission_classes import IsAdminOrDietitian, IsAdminOrDietitianOrClient


class DietPlanViewSet(ModelViewSet):
    """
    API endpoint for DietPlan table (add, edit, remove, list).
    """
    serializer_class = DietPlanSerializer
    permission_classes = [IsAdminOrDietitianOrClient]

    # Filters and search
    filter_backends = [
        DjangoFilterBackend,  # Handle filter
        SearchFilter,         # Handle search
        OrderingFilter        # Handle sort
    ]

    # Filter
    filterset_fields = ['author', 'visibility', 'meals', 'tags']

    # Search
    search_fields = ['name', 'author', 'meals', 'tags']

    # Sort
    ordering_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        # Admin sees all objects
        if user.role == 'admin':
            return DietPlan.objects.all()

        # Dietitian sees only public meals or their own meals
        if user.role == 'dietitian':
            return DietPlan.objects.filter(
                Q(author=user) | Q(visibility='public')
            )

        # Dietitian sees only public meals or their own meals
        if user.role == 'client':
            if user.diet_plan:
                return DietPlan.objects.filter(id=user.diet_plan.id)

        # In other cases, no access
        return DietPlan.objects.none()

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
