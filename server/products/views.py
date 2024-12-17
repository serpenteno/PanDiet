from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from common.permission_classes import IsAdminOrDietitian, IsAdminOrDietitianOrClient


class ProductViewSet(ModelViewSet):
    """
    API endpoint for Product table (add, edit, remove, list).
    """
    serializer_class = ProductSerializer

    # Set permissions to API
    permission_classes = [IsAdminOrDietitianOrClient]

    # Filters and search
    filter_backends = [
        DjangoFilterBackend,  # Handle filter
        SearchFilter,  # Handle search
        OrderingFilter  # Handle sort
    ]

    # Filter
    filterset_fields = ['author', 'visibility', 'nutrients', 'tags']

    # Search
    search_fields = ['name', 'mass', 'author', 'nutrients', 'tags']

    # Sort
    ordering_fields = ['name', 'mass']

    def get_queryset(self):
        user = self.request.user

        # Admin sees all objects
        if user.role == 'admin':
            return Product.objects.all()

        # Dietitian sees only public meals or their own meals
        if user.role == 'dietitian':
            return Product.objects.filter(
                Q(author=user) | Q(visibility='public')
            )

        if user.role == 'client':
            return Product.objects.filter(
                id__in=user.diet_plan.meals.all().prefetch_related('products').values_list('products__id', flat=True)
            )

        # In other cases, no access
        return Product.objects.none()

    def perform_update(self, serializer):
        # Check if the user has permission to edit the object
        obj = self.get_object()
        if obj.author != self.request.user and self.request.user.role != 'admin':
            raise PermissionDenied("You don't have permission to edit this object.")
        serializer.save()

    def perform_destroy(self, instance):
        # Check if the user has permission to delete the object
        obj = self.get_object()
        if obj.author != self.request.user and self.request.user.role != 'admin':
            raise PermissionDenied("You don't have permission to delete this object.")
        instance.delete()
