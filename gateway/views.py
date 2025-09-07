import time
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Service, RequestLog


@method_decorator(csrf_exempt, name='dispatch')
class ProxyView(View):
    def dispatch(self, request, *args, **kwargs):
        start = time.time()
        path = request.path.lstrip('/')
        
        service = self.get_service(path)
        if not service:
            return JsonResponse({'error': 'service not found'}, status=404)
        
        try:
            response = self.proxy_request(request, service, path)
            duration = (time.time() -start)*1000
            self.save_log(request, service, response, duration)
            return response
        except Exception as e:
            duration = (time.time() -start)*1000
            self.save_log(request, service, None, duration, str(e))
            return JsonResponse({'error': 'server error'}, status=500)
    
    def get_service(self, path):
        services = Service.objects.filter(is_active=True)
        for service in services:
            if path.startswith(service.path_prefix):
                return service
        return None
    
    def proxy_request(self, request, service, path):
        remaining_part = path[len(service.path_prefix):].lstrip('/')
        url = f"{service.base_url.rstrip('/')}/{remaining_part}"
        
        headers = {}
        for key, value in request.META.items():
            if key.startswith('HTTP_') and key not in ['HTTP_HOST', 'HTTP_CONNECTION']:
                name = key[5:].replace('_', '-').title()
                headers[name] = value
        
        data = request.body if request.body else None


        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=data,
            params=request.GET,
            timeout=service.timeout
        )

        
        django_resp = HttpResponse(
            content=resp.content,
            status=resp.status_code,
            content_type=resp.headers.get('content-type', 'application/json')
        )
        
        skip_headers = {'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade'}
        for key, value in resp.headers.items():
            if key.lower() not in skip_headers:
                django_resp[key] = value
        
        return django_resp


    def save_log(self, request, service, response, duration, error=None):
        RequestLog.objects.create(
            api_key=getattr(request, 'api_key', None),
            service=service,
            method=request.method,
            path=request.path,
            status_code=response.status_code if response else 500,
            duration_ms=duration,
            error_message=error
        )
