from django.contrib import admin
from announcements.models import Announcement, Image, City


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class AnnouncementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ('Информация об авторе', {
            'classes': ('wide',),
            'fields': ('author', 'contact', 'phone', 'address')
        }),
        ('Информация об услуге', {
            'classes': ('wide',),
            'fields': ('service', 'city', 'price', 'desc'),
        }),
        (None, {
            'fields': ('posted', 'views', 'views_today', 'is_active'),
        }),
    )
    list_display = ['id', 'name', 'service', 'contact', 'price', 'address', 'posted', 'phone', 'is_active']
    list_display_links = ['name']
    list_filter = ['posted', 'is_active', 'city__name']
    search_fields = ['address', 'author__username', 'contact', 'name', 'price', 'phone', 'service__name']
    inlines = [ImageInline]
    readonly_fields = ['views', 'views_today', 'posted']


admin.site.register(City)
admin.site.register(Announcement, AnnouncementAdmin)