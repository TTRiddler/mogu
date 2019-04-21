from django.urls import path
from announcements import views


urlpatterns = [
    path('<an_id>/', views.an_detail, name='an_detail'),
    path('add/new/', views.an_create, name='an_create'),
]