import re
from django import forms
from profiles.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# , AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm, PasswordChangeForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Имя*'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Фамилия*'}))
    patronymic = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Отчество'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'phone', 'placeholder': 'Телефон*'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Почта*'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Пароль*'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля*'}))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'email',
            'password1',
            'password2',
        ]
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже существует.')

        return email
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким телефоном уже существует.')

        return phone
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password2 != password1:
            raise forms.ValidationError('Пароли не совпадают.')

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'phone', 'placeholder': 'Телефон'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        username = re.sub('\D', '', username)

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError('Неправильный телефон или пароль.')
        except User.DoesNotExist:
            raise forms.ValidationError('Неправильный телефон или пароль.')