from django.contrib import admin
from .models import DietPlan, DietPlanMeals


class DietPlanMealsInLine(admin.TabularInline):
    model = DietPlanMeals
    extra = 1


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    # Columns to show in admin view
    list_display = ('name', 'description', 'get_meals', 'get_tags', 'author', 'visibility')

    # Fields that are searchable
    search_fields = ('name', 'author', 'visibility', 'meals__name', 'tags__name')

    # Fields that can be filtered
    list_filter = ('tags', 'author', 'visibility')

    # Fields that can be edited during add or put operations
    fields = ('name', 'description', 'author', 'visibility')

    # Add values that are in many to many relation
    inlines = [DietPlanMealsInLine]

    # Read-only fields
    readonly_fields = ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_dietplan_tags()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_dietplan_tags()

    def get_meals(self, obj):
        return ", ".join([str(meal) for meal in obj.meals.all()])
    get_meals.short_description = 'Meals'

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

