from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    """
    API endpoint for Product table (add, edit, remove, list).
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Set permissions to API
    permission_classes = [AllowAny]

    # Filters and search
    filter_backends = [
        DjangoFilterBackend,  # Handle filter
        SearchFilter,         # Handle search
        OrderingFilter        # Handle sort
    ]

    # Filter
    filterset_fields = ['tags', 'author', 'visibility', 'nutrients']

    # Search
    search_fields = ['name', 'tags', 'mass', 'author', 'nutrients']

    # Sort
    ordering_fields = ['name', 'mass']
