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
    path('friends/add/', views.add_friends, name='add_friends'),
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),

    path('friends/your-friends/', views.your_friends, name='your_friends'),
    path('unfollow/<int:user_id>/', views.unfollow_friend, name='unfollow_friend'),

    path('friends/requests/', views.friend_requests, name='friend_requests'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('decline-request/<int:request_id>/', views.decline_request, name='decline_request'),

    path('friends/suggested/', views.suggested_friends, name='suggested_friends'),
    
    path('friends/blocked/', views.blocked_friends, name='blocked_friends'),
    path('block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock-user/<int:user_id>/', views.unblock_user, name='unblock_user'),

    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

]
