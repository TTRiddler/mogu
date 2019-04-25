from django.shortcuts import render
from announcements.models import Announcement
from announcements.forms import MainSearchForm


def index(request):
    an_all = Announcement.objects.filter(is_active=True)
    search_form = MainSearchForm()

    context = {
        'an_all': an_all,
        'search_form': search_form,
    }

    return render(request, 'landing/index.html', context)