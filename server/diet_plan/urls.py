from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DietPlanViewSet


router = DefaultRouter()
router.register(r'diet_plans', DietPlanViewSet, basename='diet_plan')

urlpatterns = [
    path('', include(router.urls)),
]