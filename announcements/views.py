from django.shortcuts import render, get_object_or_404
from announcements.models import Announcement


def an_detail(request, an_id):
    announcement = get_object_or_404(Announcement, id=int(an_id))

    context = {
        'announcement': announcement,
    }

    return render(request, 'announcements/an_detail.html', context)


def an_create(request):

    context = {
    }

    return render(request, 'announcements/an_create.html', context)