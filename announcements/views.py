from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from announcements.models import Announcement, Image, City
from services.models import ServiceType, Service
from announcements.forms import MainSearchForm


_eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
_trans_table = dict(zip(_eng_chars, _rus_chars))
 
def fix_layout(s):
    return u''.join([_trans_table.get(c, c) for c in s])


def an_detail(request, an_id):
    announcement = get_object_or_404(Announcement, id=int(an_id))

    today = datetime.today().date()
    if today == announcement.today:
        announcement.views_today += 1
    else:
        announcement.today = today 

    announcement.views += 1
    announcement.save()

    context = {
        'announcement': announcement,
    }

    return render(request, 'announcements/an_detail.html', context)


@login_required
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


def an_type_list(request, service_type_id):
    search_form = MainSearchForm()

    service_type = ServiceType.objects.get(id=int(service_type_id))
    service_types = ServiceType.objects.all()

    services = Service.objects.filter(service_type=service_type)

    an_all = Announcement.objects.filter(service__in=services, is_active=True)

    cities = City.objects.all()

    context = {
        'service_type': service_type,
        'an_all': an_all,
        'service_types': service_types,
        'cities': cities,
        'search_form': search_form,
    }

    return render(request, 'announcements/an_type_list.html', context)


def an_list(request, service_id):
    search_form = MainSearchForm()

    service = Service.objects.get(id=int(service_id))

    an_all = Announcement.objects.filter(service=service, is_active=True)
    cities = City.objects.all()

    context = {
        'an_all': an_all,
        'service': service,
        'cities': cities,
        'search_form': search_form,
    }

    return render(request, 'announcements/service_list.html', context)


class MainSerch(View):
    def post(self, request):
        search_form = MainSearchForm(request.POST)
        q = request.POST.get('q', '')

        city_id = request.POST.get('city-select')

        city = City.objects.get(id=int(city_id))

        an_res = Announcement.objects.filter(is_active=True)
        an_res = an_res.filter(city=city)
        an_res = an_res.filter(
            Q(name__icontains=q) |
            Q(service__name__icontains=q) |
            Q(service__service_type__name__icontains=q) |
            Q(desc__icontains=q)).order_by('-posted').distinct()

        cities = City.objects.all()

        context = {
            'search_form': search_form,
            'an_res': an_res,
            'cities': cities,
        }
        return render(request, 'announcements/search_result.html', context)


def search_json(request, **kwargs):
    q = request.GET.get('q', '')

    q = fix_layout(q)
    
    service_types = ServiceType.objects.filter(name__icontains=q).distinct()
    services = Service.objects.filter(name__icontains=q).distinct()
    ans = Announcement.objects.filter(is_active=True, name__icontains=q).distinct()
    
    search_list = []
    for service_type in service_types:
        new = {'q': service_type.name}
        search_list.append(new)

    for service in services:
        new = {'q': service.name}
        search_list.append(new)

    for an in ans:
        new = {'q': an.name}
        search_list.append(new)
    
    return JsonResponse(search_list, safe=False)


class AddNewAn(View):
    def get(self, request):
        service_types = ServiceType.objects.all()

        service_type = ServiceType.objects.first()
        services_start = Service.objects.filter(service_type=service_type)

        cities = City.objects.all()

        context = {
            'service_types': service_types,
            'services_start': services_start,
            'cities': cities,
        }

        return render(request, 'announcements/an_create.html', context)

    def post(self, request):
        name = request.POST.get('name')
        author = request.user
        service_id = request.POST.get('select_service')
        service = Service.objects.get(id=int(service_id))
        price = int(request.POST.get('price'))
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        phone = request.POST.get('phone')
        city_id = request.POST.get('city-select')
        city = City.objects.get(id=int(city_id))
        desc = request.POST.get('description')

        new_an = Announcement.objects.create(
            name = name,
            author = author,
            service = service,
            price = price,
            address = address,
            contact = contact,
            phone = phone,
            desc = desc,
            city = city,
        )

        for item in request.FILES.getlist('images'):
            Image.objects.create(
                announcement = new_an,
                image = item,
            )

        return redirect('profile')

