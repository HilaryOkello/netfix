from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from services.models import Service, ServiceRequest
from django.db.models import Count

def home(request):
    most_requested = Service.objects.annotate(num_requests=Count('servicerequest')).order_by('-num_requests')[:5]
    return render(request, "main/home.html", {'most_requested': most_requested})

def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
