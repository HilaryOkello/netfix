from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    company = Company.objects.get(user=request.user)
    if company.field == 'All in One':
        choices = (
            ('Air Conditioner', 'Air Conditioner'),
            ('Carpentry', 'Carpentry'),
            ('Electricity', 'Electricity'),
            ('Gardening', 'Gardening'),
            ('Home Machines', 'Home Machines'),
            ('House Keeping', 'House Keeping'),
            ('Interior Design', 'Interior Design'),
            ('Locks', 'Locks'),
            ('Painting', 'Painting'),
            ('Plumbing', 'Plumbing'),
            ('Water Heaters', 'Water Heaters'),
        )
    else:
        choices = ((company.field, company.field),)
    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_hour = form.cleaned_data['price_hour']
            field = form.cleaned_data['field']
            s = Service(company=company, name=name, description=description,
                        price_hour=price_hour, field=field)
            s.save()
            return redirect('/')
    else:
        form = CreateNewService(choices=choices)
    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    service = Service.objects.get(id=id)
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            time = form.cleaned_data['time']
            price = service.price_hour * time
            sr = ServiceRequest(customer=customer, service=service,
                                address=address, time=time, price=price)
            sr.save()
            return redirect('/')
    else:
        form = RequestServiceForm()
    return render(request, 'services/request_service.html', {'form': form, 'service': service})
