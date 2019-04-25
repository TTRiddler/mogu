from django import forms
from announcements.models import Announcement


class MainSearchForm(forms.Form):
    an_len = len(Announcement.objects.filter(is_active=True))
    placeholder = 'Объявлений на сайте: %s' % an_len
    
    q = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'typeahead',
        'autofocus': 'autofocus',
        'placeholder': placeholder,
        'id': 'main-search'
    }))