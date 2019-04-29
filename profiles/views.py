import re
from datetime import datetime
import pytz

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from profiles.tokens import account_activation_token

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

from announcements.models import Announcement
from profiles.forms import RegisterForm, LoginForm
from profiles.models import User


@login_required
def profile(request):
    user = request.user
    active_ans = Announcement.objects.filter(author=user, is_active=True)
    not_active_ans = Announcement.objects.filter(author=user, is_active=False)

    utc = pytz.UTC
    today = utc.localize(datetime.today())

    context = {
        'active_ans': active_ans,
        'not_active_ans': not_active_ans,
        'today': today,
    }

    return render(request, 'profiles/profile.html', context)


def register(request):
    reg_success = True

    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)

        if reg_form.is_valid():
            new_user = reg_form.save(commit=False)
            new_user.first_name = reg_form.cleaned_data['first_name']
            new_user.last_name = reg_form.cleaned_data['last_name']
            new_user.patronymic = reg_form.cleaned_data['patronymic']
            new_user.email = reg_form.cleaned_data['email']
            new_user.phone = reg_form.cleaned_data['phone']
            new_user.username = re.sub('\D', '', new_user.phone)
            new_user.set_password(reg_form.cleaned_data['password2'])
            new_user.is_active = False
            new_user.save()

            try:
                current_site = get_current_site(request)
                mail_subject = 'Подтверждение почты'
                message = render_to_string('profiles/account_activate_message.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': account_activation_token.make_token(new_user),
                })
                to_email = new_user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return render(request, 'profiles/account_activate_done.html')
            except:
                return render(request, 'profiles/account_activate_mail_error.html')
        else:
            reg_success = False

            context = {
                'reg_form': reg_form,
                'reg_success': reg_success,
            }

            return render(request, 'landing/index.html', context)

    return redirect('/')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'profiles/account_activate_complete.html')
    else:
        return render(request, 'profiles/account_activate_error.html')
    

def mylogin(request):
    login_success = True

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            username = re.sub('\D', '', username)
            user = authenticate(username=username, password=password)
            login(request, user)
        else:
            login_success = False
            
            context = {
                'login_success': login_success,
                'login_form': login_form,
            }

            return render(request, 'landing/index.html', context) 
    
    return redirect('/')


def mylogout(request):
    logout(request)
    return redirect('/')
