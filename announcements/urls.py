from django.urls import path
from announcements import views


urlpatterns = [
    path('detail/<an_id>/', views.an_detail, name='an_detail'),
    path('create/', views.AddNewAn.as_view(), name='an_create'),
    path('service_choice/', views.service_choice, name='service_choice'),
    path('service_type/<service_type_id>/', views.an_type_list, name='an_type_list'),
    path('service/<service_id>/', views.an_list, name='an_list'),
    # path('search/result/', views.MainSerch.as_view(), name='main_search'),
    path('search.json', views.search_json, name='search_json'),
]