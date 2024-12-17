from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NutrientViewSet


router = DefaultRouter()
router.register(r'', NutrientViewSet, basename='nutrient')

urlpatterns = [
    path('', include(router.urls)),
]
