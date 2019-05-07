from django.urls import path
from django.contrib.auth.decorators import login_required
from profiles import views


urlpatterns = [
    path('profile/active/', views.profile, name='profile'),
    path('profile/not_active/', views.profile2, name='profile2'),
    path('add_message/', login_required(views.MessageView.as_view()), name='add_message'),
    path('register/', views.register, name='register'),
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/remove/', views.remove_favorite, name='remove_favorite'),
    path('favorites/add/', views.add_favorite, name='add_favorite'),
    path('passport/<user_id>/', views.passport, name='passport'),
    path('user_ans/<user_id>/', views.user_ans, name='user_ans'),
]