from django.contrib import admin

from . import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region']
    search_fields = ['name']
    list_filter = ['region']
    ordering = ['region', 'name']
