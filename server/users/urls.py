from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DietitianClientViewSet

router = DefaultRouter()
router.register(r'list', UserViewSet, basename='users')
router.register(r'dietitian-clients', DietitianClientViewSet, basename='dietitian-clients')

urlpatterns = [
    path('', include(router.urls)),
]

