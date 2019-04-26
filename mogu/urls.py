from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from announcements.views import search_json


admin.site.site_header = 'Mogu.su' 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('imagefit/', include('imagefit.urls')),
    path('', include('landing.urls')),
    path('announcements/', include('announcements.urls')),
    path('accounts/', include('profiles.urls')),

    path('search.json', search_json, name='search_json'),
    path('announcements/search_result/search.json', search_json, name='search_json'),
    path('announcements/service_type/<service_type_id>/search.json', search_json, name='search_json'),
    path('announcements/service/<service_id>/search.json', search_json, name='search_json'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)