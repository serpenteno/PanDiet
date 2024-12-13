from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Columns to show in admin view
    list_display = ('name',)

    # Fields that are searchable
    search_fields = ('name',)

    # Fields that can be filtered
    list_filter = ('name',)

    # Fields that can be edited during add or put operations
    fields = ('name',)
