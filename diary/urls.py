from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-entry/', views.create_entry, name='create_entry'),
    path('friends/', views.friends, name='friends'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
]
