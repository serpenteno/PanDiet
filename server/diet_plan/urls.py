from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DietPlanViewSet, DietPlanListView, DietPlanDetailView, DietPlanDatatablesView

router = DefaultRouter()
router.register(r'dietplans', DietPlanViewSet, basename='diet_plan')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('dietplans', login_required(DietPlanListView.as_view()), name='dietplans_list'),  # HTML view
    path('dietplan/<int:pk>/', login_required(DietPlanDetailView.as_view()), name='dietplan_detail'),  # HTML view
    path('api/dietplans/datatables/', DietPlanDatatablesView.as_view(), name='dietplans-datatables'),
    path('api/', include(router.urls)),
]
