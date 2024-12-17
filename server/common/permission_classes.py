from rest_framework.permissions import BasePermission
from products.models import Product


# Custom permission class for checking if user can display object
class IsAdminOrDietitian(BasePermission):
    def has_permission(self, request, view):
        # Is user logged?
        if not request.user or not request.user.is_authenticated:
            return False
        # Is user an admin or dietitian
        return request.user.role in ['admin', 'dietitian']

    def has_object_permission(self, request, view, obj):
        # Admin full permissions
        if request.user.role == 'admin':
            return True
        # Dietitian can edit their own meals
        if request.user.role == 'dietitian':
            if obj.author == request.user:
                return True
            # Dietitian can view public meals
            return obj.visibility == 'public'
        return False


# Custom permission class for checking if user can display object
class IsAdminOrDietitianOrClient(BasePermission):
    def has_permission(self, request, view):
        # Is user logged?
        if not request.user or not request.user.is_authenticated:
            return False
        # Is user an admin or dietitian or client
        return request.user.role in ['admin', 'dietitian', 'client']

    def has_object_permission(self, request, view, obj):
        # Admin full permissions
        if request.user.role == 'admin':
            return True
        # Dietitian can edit their own meals
        if request.user.role == 'dietitian':
            if obj.author == request.user:
                return True
            # Dietitian can view public meals
            return obj.visibility == 'public'
        # Client can view his diet_plan
        if request.user.role == 'client':
            if request.user.diet_plan == obj or obj in request.user.diet_plan.meals.all():
                return True
            elif obj in Product.objects.filter(meal__in=request.user.diet_plan.meals.all()):
                return True
            else:
                return False
        return False
