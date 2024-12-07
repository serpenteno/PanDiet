from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Nutrient
from .serializers import NutrientSerializer


class NutrientViewSet(ModelViewSet):
    """
    API endpoint for Nutrient table (add, edit, remove, list).
    """
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer
    # Set permissions to API
    permission_classes = [AllowAny]

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
