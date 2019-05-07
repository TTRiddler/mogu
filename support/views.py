from django.shortcuts import render, redirect
from django.views import View
from support.models import SupportMessage


class MessageView(View):
    def get(self, request):
        return render(request, 'support/support.html')
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        sup_message = SupportMessage.objects.create(
            name = name,
            email = email,
            message = message,
        )

        return redirect('/')
