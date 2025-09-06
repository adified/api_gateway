from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import APIKey


class APIAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):

        api_key = request.META.get('X-API-KEY')
        
        if not api_key:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        # validating the API key
        try:
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            request.api_key = api_key_obj
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        return None