from django.contrib import admin
from .models import Product, ProductNutrient


class ProductNutrientInline(admin.TabularInline):
    model = ProductNutrient
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns to show in admin view
    list_display = ('name', 'description', 'get_nutrients', 'get_tags', 'mass', 'author', 'visibility')

    # Fields that are searchable
    search_fields = ('name', 'mass', 'author', 'visibility', 'nutrients__name', 'tags__name')

    # Fields that can be filtered
    list_filter = ('tags', 'author', 'visibility')

    # Fields that can be edited during add or put operations
    fields = ('name', 'description', 'tags', 'mass', 'author', 'visibility')

    # Add values that are in many to many relation
    inlines = [ProductNutrientInline]

    # Read-only fields
    readonly_fields = ()

    def get_nutrients(self, obj):
        return ", ".join([str(nutrient) for nutrient in obj.nutrients.all()])
    get_nutrients.short_description = 'Nutrients'

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'
