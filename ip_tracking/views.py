from django.http import HttpResponse
from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def authenticated_view(request):
    return HttpResponse("Authenticated access granted.")

@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def anonymous_view(request):
    return HttpResponse("Anonymous access granted.")
