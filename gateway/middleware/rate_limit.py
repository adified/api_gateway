from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.conf import settings


class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):

        # ignore admin request
        if request.path.startswith(('/admin/')):
            return None
        
        # check for api_key as defined in the auth middleware
        if not hasattr(request, 'api_key'):
            return None
            
        api_key = request.api_key.key
        cache_key = f"rate_limit:{api_key}"
        
        # default is 0 if the key does not exist
        current_requests = cache.get(cache_key, 0)
        
        # Check if limit exceeded
        if current_requests >= settings.RATE_LIMIT_REQUESTS_PER_HOUR:
            return JsonResponse({'error': ' too many requests'}, status=429)
        
        # Increment counter
        cache.set(cache_key, current_requests + 1, 3600)  # 1 hour TTL
        
        return None