from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

class CustomUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.TextField()
    con_password = models.TextField()
    
    def __str__(self):
        return self.username

class DiaryEntry(models.Model):
    PRIVACY_CHOICES = [
        ('private', 'Private'),
        ('friends', 'Friends-only'),
        ('public', 'Public'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='private')

    def __str__(self):
        return self.title

class DiaryImage(models.Model):
    diary_entry = models.ForeignKey(DiaryEntry, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='diary_images/')

    def __str__(self):
        return f'Image of {self.diary_entry}'

class Friend(models.Model):
    user_from = models.ForeignKey(User, related_name='friend_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='friend_of_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_from} is friends with {self.user_to}'
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"
    

class BlockedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked')
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} blocked {self.blocked_user.username}"