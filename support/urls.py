from django.urls import path
from support import views


urlpatterns = [
    path('message/', views.MessageView.as_view(), name='message'),
]