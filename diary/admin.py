from django.contrib import admin
from .models import DiaryEntry,DiaryImage,Friend
# Register your models here.

admin.site.register(DiaryEntry)
admin.site.register(DiaryImage)
admin.site.register(Friend)