from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from announcements.models import Announcement, Image
from services.models import ServiceType, Service
from announcements.forms import MainSearchForm


_eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
_trans_table = dict(zip(_eng_chars, _rus_chars))
 
def fix_layout(s):
    return u''.join([_trans_table.get(c, c) for c in s])


def an_detail(request, an_id):
    announcement = get_object_or_404(Announcement, id=int(an_id))

    context = {
        'announcement': announcement,
    }

    return render(request, 'announcements/an_detail.html', context)


@login_required
def an_create(request):
    service_types = ServiceType.objects.all()

    service_type = ServiceType.objects.first()
    services_start = Service.objects.filter(service_type=service_type)

    context = {
        'service_types': service_types,
        'services_start': services_start,
    }

    return render(request, 'announcements/an_create.html', context)


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
    service_type = ServiceType.objects.get(id=int(service_type_id))
    service_types = ServiceType.objects.all()

    services = Service.objects.filter(service_type=service_type)

    an_all = Announcement.objects.filter(service__in=services, is_active=True)

    context = {
        'service_type': service_type,
        'an_all': an_all,
        'service_types': service_types,
    }

    return render(request, 'announcements/an_type_list.html', context)


def an_list(request, service_id):
    service = Service.objects.get(id=int(service_id))

    an_all = Announcement.objects.filter(service=service, is_active=True)

    context = {
        'an_all': an_all,
        'service': service,
    }

    return render(request, 'announcements/service_list.html', context)


# class MainSerch(View):
#     def get(self, request):
#         search_form = MainSerchForm()

#         context = {
#             'search_form': search_form,
#         }
#         return render(request, 'landing/index.html', context)

#     def post(self, request):
#         search_form = MainSerchForm(request.POST)

#         context = {
#             'search_form': search_form,
#         }
#         return render(request, 'landing/index.html', context)


def search_json(request):
    q = request.GET.get('q', '')

    q = fix_layout(q)
    
    service_types = ServiceType.objects.filter(name__icontains=q)
    services = Service.objects.filter(name__icontains=q)
    ans = Announcement.objects.filter(is_active=True, name__icontains=q)
    
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

        context = {
            'service_types': service_types,
            'services_start': services_start,
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
        )

        for item in request.FILES.getlist('images'):
            Image.objects.create(
                announcement = new_an,
                image = item,
            )

        return redirect('profile')

