from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    ip_activity = {}

    for log in logs:
        ip = log.ip_address
        ip_activity[ip] = ip_activity.get(ip, 0) + 1

        if log.path in ['/admin', '/login']:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"Accessed sensitive path: {log.path}"}
            )

    for ip, count in ip_activity.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': "More than 100 requests in 1 hour"}
            )
