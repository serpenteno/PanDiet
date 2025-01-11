from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.renderers import DatatablesRenderer

from .models import DietPlan
from .serializers import DietPlanSerializer
from common.permission_classes import IsAdminOrDietitian, IsAdminOrDietitianOrClient


class DietPlanListView(ListView):
    """
    Render page with diet plans list
    """
    model = DietPlan
    context_object_name = 'dietplans'

    def get_template_names(self):
        user_role = self.request.user.role
        if user_role in ['admin', 'dietitian']:
            return ['Dietplans.html']


class DietPlanDetailView(DetailView):
    """
    Render page with detail view/edit view
    """
    model = DietPlan
    context_object_name = 'dietplan'

    def get_template_names(self):
        user_role = self.request.user.role
        if user_role in ['admin', 'dietitian']:
            return ['DietPlanEdit.html']
        elif user_role == "client":
            return ['DietPlanDisplay.html']
        else:
            return


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
    search_fields = ['name', 'meals__name', 'tags__name']

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


class DietPlanDatatablesView(generics.ListAPIView):
    """
    API endpoint specific for Dietplan data table from JQuery (display).
    """
    serializer_class = DietPlanSerializer
    renderer_classes = [DatatablesRenderer, JSONRenderer]
    pagination_class = DatatablesPageNumberPagination
    filter_backends = [DatatablesFilterBackend]
    permission_classes = [IsAdminOrDietitianOrClient]

    search_fields = ['name', 'author__name', 'meals__name', 'tags__name']

    def get_queryset(self):
        user = self.request.user

        # Permission logic
        if user.role == 'admin':
            qs = DietPlan.objects.all()
        elif user.role == 'dietitian':
            qs = DietPlan.objects.filter(Q(author=user) | Q(visibility='public'))
        elif user.role == 'client':
            qs = DietPlan.objects.filter(
                id__in=user.diet_plan.meals.all().prefetch_related('products')
                      .values_list('products__id', flat=True)
            )
        else:
            qs = DietPlan.objects.none()

        return qs
