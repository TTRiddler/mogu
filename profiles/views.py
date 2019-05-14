import re

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils import timezone
from django.views import View
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

from announcements.models import Announcement
from profiles.forms import RegisterForm, LoginForm, ProfileEditForm
from profiles.tokens import account_activation_token
from profiles.models import User, FavoriteAn, Message, MessageType, MessageImage
from landing.pagination import pagination


@login_required
def profile(request):
    user = request.user
    active_ans = Announcement.objects.filter(author=user, is_active=True)

    today = timezone.now()

    page_number = request.GET.get('page', 1)
    pag_res = pagination(active_ans, page_number)

    thanks_type = MessageType.objects.get(name__icontains='Благодарность')
    complaints_type = MessageType.objects.get(name__icontains='Жалоба')
    claims_type = MessageType.objects.get(name__icontains='Претензия')

    thanks = Message.objects.filter(is_active=True, about=user, message_type=thanks_type)
    complaints = Message.objects.filter(is_active=True, about=user, message_type=complaints_type)
    claims = Message.objects.filter(is_active=True, about=user, message_type=claims_type)

    thanks_len = len(thanks)
    complaints_len = len(complaints)
    claims_len = len(claims)

    context = {
        'active_ans': active_ans,
        'today': today,

        'page_object': pag_res['page'],
        'is_paginated': pag_res['is_paginated'],
        'next_url': pag_res['next_url'],
        'prev_url': pag_res['prev_url'],

        'thanks_len': thanks_len,
        'complaints_len': complaints_len,
        'claims_len': claims_len,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def profile2(request):
    user = request.user
    not_active_ans = Announcement.objects.filter(author=user, is_active=False)

    today = timezone.now()
    
    page_number = request.GET.get('page', 1)
    pag_res = pagination(not_active_ans, page_number)

    thanks_type = MessageType.objects.get(name__icontains='Благодарность')
    complaints_type = MessageType.objects.get(name__icontains='Жалоба')
    claims_type = MessageType.objects.get(name__icontains='Претензия')

    thanks = Message.objects.filter(is_active=True, about=user, message_type=thanks_type)
    complaints = Message.objects.filter(is_active=True, about=user, message_type=complaints_type)
    claims = Message.objects.filter(is_active=True, about=user, message_type=claims_type)

    thanks_len = len(thanks)
    complaints_len = len(complaints)
    claims_len = len(claims)

    context = {
        'not_active_ans': not_active_ans,
        'today': today,

        'page_object': pag_res['page'],
        'is_paginated': pag_res['is_paginated'],
        'next_url': pag_res['next_url'],
        'prev_url': pag_res['prev_url'],

        'thanks_len': thanks_len,
        'complaints_len': complaints_len,
        'claims_len': claims_len,
    }

    return render(request, 'profiles/profile2.html', context)


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


@login_required
def mylogout(request):
    logout(request)
    return redirect('/')


@login_required
def favorites(request):
    user = request.user
    favorites = FavoriteAn.objects.filter(user=user)
    ans = [an.announcement for an in favorites]

    context = {
        'ans': ans,
    }

    return render(request, 'profiles/favorites.html', context)


@login_required
def remove_favorite(request):
    user = request.user
    an_id = request.GET.get('an_id')
    an = Announcement.objects.get(id=int(an_id))
    
    favorite = FavoriteAn.objects.get(user=user, announcement=an)
    favorite.delete()

    return redirect('favorites')


@login_required
def add_favorite(request):
    user = request.user
    an_id = request.GET.get('an_id')
    an = Announcement.objects.get(id=int(an_id))
    
    favorite = FavoriteAn.objects.update_or_create(user=user, announcement=an)

    return redirect('/announcements/detail/%s/' % an.id)


def passport(request, user_id):
    some_user = get_object_or_404(User, id=int(user_id))

    thanks_type = MessageType.objects.get(name__icontains='Благодарность')
    complaints_type = MessageType.objects.get(name__icontains='Жалоба')
    claims_type = MessageType.objects.get(name__icontains='Претензия')


    thanks = Message.objects.filter(is_active=True, about=some_user, message_type=thanks_type)
    complaints = Message.objects.filter(is_active=True, about=some_user, message_type=complaints_type)
    claims = Message.objects.filter(is_active=True, about=some_user, message_type=claims_type)

    context = {
        'some_user': some_user,
        'thanks': thanks,
        'complaints': complaints,
        'claims': claims,
        'thanks_type': thanks_type,
        'complaints_type': complaints_type,
        'claims_type': claims_type,
    }

    return render(request, 'profiles/passport.html', context)


def user_ans(request, user_id):
    some_user = get_object_or_404(User, id=int(user_id))

    ans = Announcement.objects.filter(is_active=True, author=some_user)

    context = {
        'ans': ans,
        'some_user': some_user,
    }

    return render(request, 'profiles/user_ans.html', context)


class MessageView(View):
    def get(self, request):
        message_type_id = request.GET.get('message_type_id')
        about_id = request.GET.get('about_id')

        message_type = MessageType.objects.get(id=int(message_type_id))
        some_user = User.objects.get(id=int(about_id))

        author = request.user
        about = some_user

        context = {
            'message_type': message_type,
            'author': author,
            'about': about,
        }

        return render(request, 'profiles/add_message.html', context)

    def post(self, request):
        about_id = request.POST.get('about_id')
        author_id = request.POST.get('author_id')
        message_type_id = request.POST.get('message_type_id')
        text = request.POST.get('text')

        about = get_object_or_404(User, id=int(about_id))
        author = get_object_or_404(User, id=int(author_id))
        message_type = get_object_or_404(MessageType, id=int(message_type_id))

        message = Message.objects.create(
            message_type=message_type,
            author=author,
            about=about,
            text=text,
        )

        MessageImage.objects.filter(message=message).delete()

        for item in request.FILES.getlist('images'):
            MessageImage.objects.create(
                message = message,
                image = item,
            )

        return redirect('/accounts/passport/%s/' % about_id)


class ProfileEditView(View):
    def get(self, request):
        profile_edit_form = ProfileEditForm(user=request.user)

        context = {
            'profile_edit_form': profile_edit_form,
        }

        return render(request, 'profiles/profile_edit.html', context)

    def post(self, request):
        profile_edit_form = ProfileEditForm(request.user, request.POST, request.FILES)

        if profile_edit_form.is_valid():
            user = request.user
            user.first_name = profile_edit_form.cleaned_data['first_name']
            user.last_name = profile_edit_form.cleaned_data['last_name']
            user.patronymic = profile_edit_form.cleaned_data['patronymic']
            user.photo = profile_edit_form.cleaned_data['photo']
            user.save()

        return redirect('profile')


class PasswordReset(PasswordResetView):
    template_name = 'profiles/password_reset.html'

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'profiles/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'profiles/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'profiles/password_reset_complete.html'
