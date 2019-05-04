from django.urls import path
from profiles import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/remove/', views.remove_favorite, name='remove_favorite'),
    path('favorites/add/', views.add_favorite, name='add_favorite'),
]