from django.urls import path
from django.contrib.auth.decorators import login_required
from profiles import views


urlpatterns = [
    path('profile/active/', views.profile, name='profile'),
    path('profile/not_active/', views.profile2, name='profile2'),
    path('profile/edit/', login_required(views.ProfileEditView.as_view()), name='profile_edit'),
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

    path('password-reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password-reset-done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password-reset-complete', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]