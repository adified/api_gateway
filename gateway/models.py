from django.db import models
import secrets


def generate_api_key():
    return secrets.token_urlsafe(32)

# Create your models here.
class APIKey(models.Model):
    """model to store API keys for auth"""
    key = models.CharField(max_length=64, unique=True, default=generate_api_key)
    name = models.CharField(max_length=100, help_text="name for API keys")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.key[:8]}...)"
    
    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"


class Service(models.Model):
    """model to store downstream service configs"""
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(help_text="base URL of the service")
    path_prefix = models.CharField(max_length=200, help_text="path prefix for routing like api/v1/users",unique=True)
    is_active = models.BooleanField(default=True)
    timeout = models.IntegerField(default=30, help_text="request timeout duration")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.path_prefix})"
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

class RequestLog(models.Model):
    """model to store request logs"""
    timestamp = models.DateTimeField(auto_now_add=True)
    api_key = models.ForeignKey(APIKey, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    error_message = models.TextField(blank=True, null=True)
    duration_ms = models.FloatField(help_text="Request duration in milliseconds")
    
    def __str__(self):
        return f"{self.method} {self.path} - {self.status_code} ({self.timestamp})"
    
    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']