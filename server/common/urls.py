from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import CustomLoginView, LogoutView, IndexView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('', IndexView.as_view(), name='index'),
]
