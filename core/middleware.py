from django.core.cache import cache
from django.http import JsonResponse

class RateLimitMiddleware:
    """
    Middleware to limit the rate of incoming requests from a single IP address.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 100  # Max requests
        self.time_window = 60  # Time window in seconds

    def __call__(self, request):
        ip_address = self.get_client_ip(request)

        if request.path.startswith('/api/'):
            if self.is_rate_limited(ip_address):
                return JsonResponse(
                    {"error": "Rate limit exceeded. Try again later."},
                    status=429
                )

        
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_rate_limited(self, ip):
        cache_key = f"rate_limit_{ip}"
        request_count = cache.get(cache_key)

        if request_count:
            if request_count >= self.rate_limit:
                return True
            cache.incr(cache_key)
        else:
            cache.set(cache_key, 1, timeout=self.time_window)
        return False