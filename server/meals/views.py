from django.db.models import Q
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.renderers import DatatablesRenderer

from .models import Meal
from .serializers import MealSerializer
from common.permission_classes import IsAdminOrDietitian, IsAdminOrDietitianOrClient


class MealListView(ListView):
    model = Meal
    context_object_name = 'meals'
    def get_template_names(self):
        user_role = self.request.user.role
        if user_role in ['admin', 'dietitian']:
            return ['meals.html']


class MealViewSet(ModelViewSet):
    """
    API endpoint for Meal table (add, edit, remove, list).
    """
    serializer_class = MealSerializer
    permission_classes = [IsAdminOrDietitianOrClient]

    # Filters and search
    filter_backends = [
        DjangoFilterBackend,  # Handle filter
        SearchFilter,         # Handle search
        OrderingFilter        # Handle sort
    ]

    # Filter
    filterset_fields = ['author', 'visibility', 'products', 'tags']

    # Search
    search_fields = ['name', 'mass', 'author', 'products__name', 'tags__name']

    # Sort
    ordering_fields = ['name', 'mass']

    def get_queryset(self):
        user = self.request.user

        # Admin sees all objects
        if user.role == 'admin':
            return Meal.objects.all()

        # Dietitian sees only public meals or their own meals
        if user.role == 'dietitian':
            return Meal.objects.filter(
                Q(author=user) | Q(visibility='public')
            )

        if user.role == 'client':
            return Meal.objects.filter(
                Q(id__in=user.diet_plan.meals.values_list('id', flat=True))
            )

        # In other cases, no access
        return Meal.objects.none()

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


class MealDatatablesView(generics.ListAPIView):
    """
    API endpoint specific for Meal data table from JQuery (display).
    """
    serializer_class = MealSerializer
    renderer_classes = [DatatablesRenderer, JSONRenderer]
    pagination_class = DatatablesPageNumberPagination
    filter_backends = [DatatablesFilterBackend]
    permission_classes = [IsAdminOrDietitianOrClient]

    # Search
    search_fields = ['name', 'mass', 'products__name', 'tags__name']

    def get_queryset(self):
        user = self.request.user

        # Permissions logic
        if user.role == 'admin':
            qs = Meal.objects.all()
        elif user.role == 'dietitian':
            qs = Meal.objects.filter(Q(author=user) | Q(visibility='public'))
        elif user.role == 'client':
            qs = Meal.objects.filter(
                id__in=user.diet_plan.meals.all().prefetch_related('products')
                      .values_list('products__id', flat=True)
            )
        else:
            qs = Meal.objects.none()

        return qs
