from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, DietitianClient
from .serializers import UserSerializer, DietitianClientSerializer
from common.permission_classes import IsAdminOrDietitian


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
