from django.contrib import admin
from .models import Meal, MealProducts

class MealProductsInLine(admin.TabularInline):
    model = MealProducts
    extra = 1


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    # Columns to show in admin view
    list_display = ('name', 'description', 'get_products', 'recipe', 'mass', 'author', 'visibility')

    # Fields that are searchable
    search_fields = ('name', 'mass', 'author', 'visibility', 'products__name')

    # Fields that can be filtered
    list_filter = ('author', 'visibility')

    # Fields that can be edited during add or put operations
    fields = ('name', 'description', 'recipe', 'mass', 'author', 'visibility')

    # Add values that are in many to many relation
    inlines = [MealProductsInLine]

    # Read-only fields
    readonly_fields = ()

    def get_products(self, obj):
        return ", ".join([str(product) for product in obj.products.all()])
    get_products.short_description = 'Products'