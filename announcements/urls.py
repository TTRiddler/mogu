from django.urls import path
from announcements import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('detail/<an_id>/', views.an_detail, name='an_detail'),
    path('create/', login_required(views.AddNewAn.as_view()), name='an_create'),
    path('service_choice/', views.service_choice, name='service_choice'),
    path('service_type/<service_type_id>/', views.an_type_list, name='an_type_list'),
    path('service/<service_id>/', views.an_list, name='an_list'),
    path('search_result/', views.MainSerch.as_view(), name='search_result'),
]