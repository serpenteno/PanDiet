from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DietPlanViewSet


router = DefaultRouter()
router.register(r'', DietPlanViewSet, basename='diet_plan')

urlpatterns = [
    path('', include(router.urls)),
]