from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Meal
from .serializers import MealSerializer


class MealViewSet(ModelViewSet):
    """
    API endpoint for Meal table (add, edit, remove, list).
    """
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    # Set permissions to API
    permission_classes = [AllowAny]

    # Filters and search
    filter_backends = [
        DjangoFilterBackend,  # Handle filter
        SearchFilter,         # Handle search
        OrderingFilter        # Handle sort
    ]

    # Filter
    filterset_fields = ['tags', 'author', 'visibility', 'products']

    # Search
    search_fields = ['name', 'tags', 'mass', 'author', 'products']

    # Sort
    ordering_fields = ['name', 'mass']
