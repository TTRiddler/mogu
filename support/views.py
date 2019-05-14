from django.shortcuts import render, redirect
from django.views import View

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

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

        current_site = get_current_site(request)
        mail_subject = 'Сообщение в тех. поддержку'
        message = render_to_string('support/mail_sup.html', {
            'sup_message': sup_message,
            'domain': current_site.domain,
        })
        to_email = sup_message.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()  

        return redirect('/')
