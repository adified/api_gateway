from django.contrib import admin
from .models import APIKey, Service, RequestLog


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'key']
    readonly_fields = ['key', 'created_at', 'updated_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'path_prefix', 'base_url', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'path_prefix', 'base_url']


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'method', 'path', 'status_code', 'duration_ms', 'api_key', 'service']
    list_filter = ['status_code', 'method', 'timestamp', 'api_key', 'service']
    search_fields = ['path', 'api_key__name', 'service__name']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'