from django.contrib import admin
from support.models import SupportMessage


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date']