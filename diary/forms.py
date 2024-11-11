from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import DiaryEntry, Profile, DiaryImage

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

class DiaryEntryForm(forms.ModelForm):

    class Meta:
        model = DiaryEntry
        fields = ['content', 'privacy',]

class DiaryImageForm(forms.Form):
    images = forms.ImageField(required=False)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
