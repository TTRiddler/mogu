from django.urls import path
from announcements import views


urlpatterns = [
    path('detail/<an_id>/', views.an_detail, name='an_detail'),
    path('add/new/', views.an_create, name='an_create'),
    path('service_choice/', views.service_choice, name='service_choice'),
]