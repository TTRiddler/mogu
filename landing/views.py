from django.shortcuts import render
from announcements.models import Announcement, City
from announcements.forms import MainSearchForm


def index(request):
    an_all = Announcement.objects.filter(is_active=True)
    cities = City.objects.all()
    search_form = MainSearchForm()

    context = {
        'an_all': an_all,
        'search_form': search_form,
        'cities': cities,
    }

    return render(request, 'landing/index.html', context)