from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.renderers import DatatablesRenderer

from .models import Product
from .serializers import ProductSerializer
from common.permission_classes import IsAdminOrDietitian, IsAdminOrDietitianOrClient


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'

    def get_template_names(self):
        user_role = self.request.user.role
        if user_role in ['admin', 'dietitian']:
            return ['products.html']


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
    search_fields = ['name', 'mass', 'tags__name', 'nutrients__name']

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


class ProductDatatablesView(generics.ListAPIView):
    """
    API endpoint specific for Product data table from JQuery (display).
    """
    serializer_class = ProductSerializer
    renderer_classes = [DatatablesRenderer, JSONRenderer]
    pagination_class = DatatablesPageNumberPagination
    filter_backends = [DatatablesFilterBackend]
    permission_classes = [IsAdminOrDietitianOrClient]

    search_fields = ['name', 'mass', 'tags__name', 'nutrients__name']

    def get_queryset(self):
        user = self.request.user

        # Permissions logic
        if user.role == 'admin':
            qs = Product.objects.all()
        elif user.role == 'dietitian':
            qs = Product.objects.filter(Q(author=user) | Q(visibility='public'))
        elif user.role == 'client':
            qs = Product.objects.filter(
                id__in=user.diet_plan.meals.all().prefetch_related('products')
                      .values_list('products__id', flat=True)
            )
        else:
            qs = Product.objects.none()

        return qs
