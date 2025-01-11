from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet


router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('api/', include(router.urls)),
]
