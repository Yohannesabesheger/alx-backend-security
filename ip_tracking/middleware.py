from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden
from django.core.cache import cache
import datetime
import requests

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Check geolocation from cache or external API
        geo_data = cache.get(f"geo:{ip}")
        country, city = None, None

        if not geo_data:
            try:
                response = requests.get(f"https://ipapi.co/{ip}/json/")
                if response.status_code == 200:
                    data = response.json()
                    country = data.get("country_name")
                    city = data.get("city")
                    cache.set(f"geo:{ip}", {'country': country, 'city': city}, 86400)
            except Exception:
                pass
        else:
            country = geo_data.get("country")
            city = geo_data.get("city")

        # Save request log
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=datetime.datetime.now(),
            path=request.path,
            country=country,
            city=city
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
