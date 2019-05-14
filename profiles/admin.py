from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from profiles.models import User, FavoriteAn, Message, MessageImage, MessageType, StarColor


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'patronymic', 'phone', 'email', 'photo', 'star_color')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class MessageImageInline(admin.TabularInline):
    model = MessageImage
    extra = 0


class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_type', 'author', 'about', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    inlines = [MessageImageInline]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(FavoriteAn)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageType)
admin.site.register(StarColor)