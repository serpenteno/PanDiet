from django.views.generic import ListView, DetailView
from rest_framework import viewsets, filters, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.renderers import DatatablesRenderer

from .models import User, DietitianClient
from .serializers import UserSerializer, DietitianClientSerializer
from common.permission_classes import IsAdminOrDietitian, UsersEdit


class UserListView(ListView):
    """
    Render page with users list
    """
    model = User
    context_object_name = 'users'

    def get_template_names(self):
        user_role = self.request.user.role
        if user_role in ['admin', 'dietitian']:
            return ['clients.html']
        else:
            return


class UserDetailView(DetailView):
    """
    Render page with detail view/edit view of user
    """
    model = User
    context_object_name = 'user'

    def get_template_names(self):
        user_role = self.request.user.role
        if user_role in ['admin', 'dietitian']:
            return ['profile.html']
        elif user_role == "client":
            return ['profile.html']
        else:
            return


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Set permissions to API
    permission_classes = [IsAdminOrDietitian]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'email']
    ordering = ['id']

    def get_queryset(self):
        if self.request.user.role == 'dietitian':
            return User.objects.filter(dietitians__dietitian=self.request.user)
        return super().get_queryset()


class DietitianClientViewSet(viewsets.ModelViewSet):
    queryset = DietitianClient.objects.all()

    # Set permissions to API
    permission_classes = [IsAdminOrDietitian]

    serializer_class = DietitianClientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['dietitian', 'client']
    search_fields = ['dietitian__username', 'client__username']
    ordering_fields = ['id', 'dietitian', 'client']
    ordering = ['id']


class UserDatatablesView(generics.ListAPIView):
    """
    API endpoint specific for User data table from JQuery (display).
    """
    serializer_class = UserSerializer
    renderer_classes = [DatatablesRenderer, JSONRenderer]
    pagination_class = DatatablesPageNumberPagination
    filter_backends = [DatatablesFilterBackend]
    permission_classes = [IsAdminOrDietitian]

    def get_queryset(self):
        user = self.request.user

        # Permissions logic
        if user.role == 'admin':
            qs = User.objects.all()
        elif user.role == 'dietitian':
            qs = User.objects.filter(Q(dietitian=user))
        else:
            qs = User.objects.none()

        return qs
