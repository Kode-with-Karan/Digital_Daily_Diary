from django.contrib import admin
from .models import DiaryEntry,DiaryImage,Friend,FriendRequest,BlockedUser,CustomUser
# Register your models here.

admin.site.register(DiaryEntry)
admin.site.register(DiaryImage)
admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(BlockedUser)
admin.site.register(CustomUser)