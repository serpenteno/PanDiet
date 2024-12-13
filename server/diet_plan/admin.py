from django.contrib import admin
from .models import DietPlan, DietPlanMeals

class DietPlanMealsInLine(admin.TabularInline):
    model = DietPlanMeals
    extra = 1


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    # Columns to show in admin view
    list_display = ('name', 'description', 'get_meals', 'author', 'visibility')

    # Fields that are searchable
    search_fields = ('name', 'author', 'visibility', 'meals__name')

    # Fields that can be filtered
    list_filter = ('author', 'visibility')

    # Fields that can be edited during add or put operations
    fields = ('name', 'description', 'author', 'visibility')

    # Add values that are in many to many relation
    inlines = [DietPlanMealsInLine]

    # Read-only fields
    readonly_fields = ()

    def get_meals(self, obj):
        return ", ".join([str(meal) for meal in obj.meals.all()])
    get_meals.short_description = 'Meals'