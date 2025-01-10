from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealViewSet, MealListView

router = DefaultRouter()
router.register(r'meals', MealViewSet, basename='meal')

urlpatterns = [
    path('meals', MealListView.as_view(), name='meal_list'),  # HTML view
    path('api/', include(router.urls)),
]
