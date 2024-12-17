from django.contrib import admin
from .models import Meal, MealProducts


class MealProductsInLine(admin.TabularInline):
    model = MealProducts
    extra = 1


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    # Columns to show in admin view
    list_display = ('name', 'description', 'get_products', 'get_tags', 'recipe', 'mass', 'author', 'visibility')

    # Fields that are searchable
    search_fields = ('name', 'mass', 'author', 'visibility', 'products__name', 'tags__name')

    # Fields that can be filtered
    list_filter = ('tags', 'author', 'visibility')

    # Fields that can be edited during add or put operations
    fields = ('name', 'description', 'recipe', 'mass', 'author', 'visibility')

    # Add values that are in many to many relation
    inlines = [MealProductsInLine]

    # Read-only fields
    readonly_fields = ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_meal_tags()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_meal_tags()

    def get_products(self, obj):
        return ", ".join([str(product) for product in obj.products.all()])
    get_products.short_description = 'Products'

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

