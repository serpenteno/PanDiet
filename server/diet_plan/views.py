from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import DietPlan
from .serializers import DietPlanSerializer


class DietPlanViewSet(ModelViewSet):
    """
    API endpoint for DietPlan table (add, edit, remove, list).
    """
    queryset = DietPlan.objects.all()
    serializer_class = DietPlanSerializer

    # Set permissions to API
    permission_classes = [AllowAny]

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
