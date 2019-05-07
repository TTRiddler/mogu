import locale

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from announcements.models import Announcement, Image, City
from services.models import ServiceType, Service
from announcements.forms import MainSearchForm
from landing.pagination import pagination
from profiles.models import FavoriteAn


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

    user = request.user
    if FavoriteAn.objects.filter(user=user, announcement=announcement).exists():
        in_favorite = True
    else:
        in_favorite = False

    user_ans = Announcement.objects.filter(is_active=True, author=announcement.author)
    user_an_count = len(user_ans)
    
    context = {
        'announcement': announcement,
        'in_favorite': in_favorite,
        'user_an_count': user_an_count,
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


def main_search(request):
    search_form = MainSearchForm(request.GET)
    q = request.GET.get('q', '')

    q = fix_layout(q)

    city_id = request.GET.get('city-select')
    sort = request.GET.get('sort_by', '3')

    city = City.objects.get(id=int(city_id))

    an_res = Announcement.objects.filter(is_active=True)
    an_res = an_res.filter(city=city)
    an_res = an_res.filter(
        Q(name__icontains=q) |
        Q(service__name__icontains=q) |
        Q(service__service_type__name__icontains=q) |
        Q(desc__icontains=q)).order_by('-posted').distinct()

    if sort == '1':
        an_res = an_res.order_by('price')
    if sort == '2':
        an_res = an_res.order_by('-price')

    cities = City.objects.all()

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    an_res_prices = [an.price for an in an_res]

    if min_price:
        min_price = int(min_price)
        an_res = [an for an in an_res if an.price>=int(min_price)]
    else:
        min_price = min(an_res_prices)

    if max_price:
        max_price = int(max_price)
        an_res = [an for an in an_res if an.price<=int(max_price)]
    else:
        max_price = max(an_res_prices)

    page_number = request.GET.get('page', 1)
    pag_res = pagination(an_res, page_number)

    request_get_string = ''
    for request_get_keys in request.GET.keys():
        if request_get_keys != 'page':
            request_get_string +=  '&' + request_get_keys + '=' + request.GET.get(request_get_keys)
    
    context = {
        'search_form': search_form,
        'cities': cities,
        'city_id': city.id,
        'request_get_string': request_get_string,
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price,

        'page_object': pag_res['page'],
        'is_paginated': pag_res['is_paginated'],
        'next_url': pag_res['next_url'],
        'prev_url': pag_res['prev_url'],
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
        can_edit = timezone.now() + datetime.timedelta(days=1)

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
            can_edit = can_edit,
        )

        Image.objects.filter(announcement=new_an).delete()

        for item in request.FILES.getlist('images'):
            Image.objects.create(
                announcement = new_an,
                image = item,
            )

        return redirect('profile')


def do_not_active(request):
    an_id = request.GET.get('an_id')

    an = Announcement.objects.get(id=int(an_id))

    an.is_active = False
    an.save()

    return JsonResponse({})


def do_active(request):
    an_id = request.GET.get('an_id')

    an = Announcement.objects.get(id=int(an_id))

    an.is_active = True
    an.save()

    return JsonResponse({})


def update(request):
    an_id = request.GET.get('an_id')

    an = Announcement.objects.get(id=int(an_id))
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    if an.posted.date() < timezone.now().date():
        an.posted = timezone.now()
        an.save()
    posted = an.posted.strftime("%d %b %Y г. %H:%M")

    context = {
        'posted': posted,
    }

    return JsonResponse(context)


class AnUpdate(View):
    def get(self, request):
        an_id = request.GET.get('an_id')

        an = Announcement.objects.get(id=int(an_id))

        service_types = ServiceType.objects.all()

        service_type = an.service.service_type
        services_start = Service.objects.filter(service_type=service_type)
        service = an.service
        cities = City.objects.all()
        city = an.city

        context = {
            'an': an,
            'service_types': service_types,
            'service_type': service_type,
            'services_start': services_start,
            'cities': cities,
            'city': city,
            'service': service,
        }

        return render(request, 'announcements/edit.html', context)

    def post(self, request):
        id = request.POST.get('id')
        author = request.user

        an = get_object_or_404(
            Announcement,
            id = int(id),
            author = author,
        )

        service_id = request.POST.get('select_service')
        city_id = request.POST.get('city-select')

        an.name = request.POST.get('name')
        an.service = Service.objects.get(id=int(service_id))
        an.price = int(request.POST.get('price'))
        an.address = request.POST.get('address')
        an.contact = request.POST.get('contact')
        an.phone = request.POST.get('phone')
        an.city = City.objects.get(id=int(city_id))
        an.desc = request.POST.get('description')
        an.posted = timezone.now()
        

        an.save()

        Image.objects.filter(announcement=an).delete()

        for item in request.FILES.getlist('images'):
            Image.objects.create(
                announcement = an,
                image = item,
            )

        return redirect('profile')

