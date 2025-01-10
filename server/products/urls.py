from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductListView


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('products', ProductListView.as_view(), name='product_list'),  # HTML view
    path('api/', include(router.urls)),
]
