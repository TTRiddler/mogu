from django.urls import path
from announcements import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('detail/<an_id>/', views.an_detail, name='an_detail'),
    path('create/', login_required(views.AddNewAn.as_view()), name='an_create'),
    path('service_choice/', views.service_choice, name='service_choice'),
    path('search_result/', views.main_search, name='search_result'),
    path('do/not_active/', views.do_not_active, name='do_not_active'),
    path('do/active/', views.do_active, name='do_active'),
    path('edit/', login_required(views.AnUpdate.as_view()), name='edit'),
]