from django.contrib import admin
from .models import Nutrient


@admin.register(Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    # Columns to show in admin view
    list_display = ('id', 'name', 'unit')

    # Fields that are searchable
    search_fields = ('name',)

    # Fields that can be filtered
    list_filter = ('unit',)

    # Fields that can be edited during add or put operations
    fields = ('name', 'unit')

    # Read-only fields
    readonly_fields = ()
