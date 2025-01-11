from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealViewSet, MealListView, MealDatatablesView

router = DefaultRouter()
router.register(r'meals', MealViewSet, basename='meal')

urlpatterns = [
    path('meals', login_required(MealListView.as_view()), name='meals_list'),  # HTML view
    path('api/meals/datatables/', MealDatatablesView.as_view(), name='meals-datatables'),
    path('api/', include(router.urls)),
]
