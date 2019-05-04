from django.shortcuts import render
from announcements.models import Announcement, City
from announcements.forms import MainSearchForm
from landing.pagination import pagination


def index(request):
    an_all = Announcement.objects.filter(is_active=True)
    cities = City.objects.all()
    search_form = MainSearchForm()

    page_number = request.GET.get('page', 1)
    pag_res = pagination(an_all, page_number)

    context = {
        'an_all': an_all,
        'search_form': search_form,
        'cities': cities,

        'page_object': pag_res['page'],
        'is_paginated': pag_res['is_paginated'],
        'next_url': pag_res['next_url'],
        'prev_url': pag_res['prev_url'],
    }

    return render(request, 'landing/index.html', context)