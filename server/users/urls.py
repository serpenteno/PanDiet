from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DietitianClientViewSet, UserListView, UserDetailView, UserDatatablesView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'dietitian-clients', DietitianClientViewSet, basename='dietitian-clients')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('clients', login_required(UserListView.as_view()), name='users_list'),  # HTML view
    path('api/users/datatables', login_required(UserDatatablesView.as_view()), name='users-datatables'),
    path('profile/<int:pk>/', login_required(UserDetailView.as_view()), name='profile'),
    path('api/', include(router.urls)),
]
