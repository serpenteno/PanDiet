from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Tag
from .serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated
from common.permission_classes import IsAdminOrDietitianOrClient


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    # Set permissions to API
    permission_classes = [IsAdminOrDietitianOrClient]

    search_fields = ['name']

    # Filters and search
    filter_backends = [
        DjangoFilterBackend,  # Handle filter
        SearchFilter,  # Handle search
        OrderingFilter  # Handle sort
    ]