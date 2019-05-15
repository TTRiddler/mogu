from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from profiles.models import User, FavoriteAn, Message, MessageImage, MessageType, StarColor


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'patronymic', 'phone', 'email', 'photo')}),
        ('Пасспорт надежности', {'fields': ('is_verified', 'star_color', 'thanks', 'complaints', 'claims')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ['thanks', 'complaints', 'claims']


class MessageImageInline(admin.TabularInline):
    model = MessageImage
    extra = 0


class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_type', 'author', 'about', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active', 'message_type']
    search_fields = ['message_type__name', 'author__username', 'about__username']
    inlines = [MessageImageInline]


class StarColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color']
    list_display_links = ['id', 'name']


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(FavoriteAn)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageType)
admin.site.register(StarColor, StarColorAdmin)