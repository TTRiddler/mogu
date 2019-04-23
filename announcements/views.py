from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from announcements.models import Announcement
from services.models import ServiceType, Service


def an_detail(request, an_id):
    announcement = get_object_or_404(Announcement, id=int(an_id))

    context = {
        'announcement': announcement,
    }

    return render(request, 'announcements/an_detail.html', context)


def an_create(request):
    service_types = ServiceType.objects.all()

    service_type = ServiceType.objects.first()
    services_start = Service.objects.filter(service_type=service_type)

    context = {
        'service_types': service_types,
        'services_start': services_start,
    }

    return render(request, 'announcements/an_create.html', context)


def service_choice(request):
    service_type_id = request.GET.get('service_type_id')
    service_type = ServiceType.objects.get(id=int(service_type_id))

    services = Service.objects.filter(service_type=service_type)
    
    services_id = [item.id for item in services]
    services_name = [item.name for item in services]

    context = {
        'services_id': services_id,
        'services_name': services_name,
    }

    return JsonResponse(context)