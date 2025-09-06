from django.db import models
import secrets

# Create your models here.
class APIKey(models.Model):
    """model to store API keys for auth"""
    key = models.CharField(max_length=64, unique=True, default=lambda: secrets.token_urlsafe(32))
    name = models.CharField(max_length=100, help_text="name for API keys")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.key[:8]}...)"
    
    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"