from django.contrib import admin
from services.models import ServiceType, Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0


class ServiceTypeAdmin(admin.ModelAdmin):
    inlines = [ServiceInline]


admin.site.register(ServiceType, ServiceTypeAdmin)