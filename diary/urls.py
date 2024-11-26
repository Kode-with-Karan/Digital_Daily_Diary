from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('diary/', views.diary, name='diary'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-entry/', views.create_entry, name='create_entry'),
    path('friends/', views.friends, name='friends'),
    path('friends/follow/', views.friends_follow, name='friends_follow'),
    path('friends/unfollow/', views.friends_unfollow, name='friends_unfollow'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
