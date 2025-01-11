from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductListView, ProductDatatablesView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('products', login_required(ProductListView.as_view()), name='products_list'),  # HTML view
    path('api/products/datatables/', ProductDatatablesView.as_view(), name='products-datatables'),
    path('api/', include(router.urls)),
]
