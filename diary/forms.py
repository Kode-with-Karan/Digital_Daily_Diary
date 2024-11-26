from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DiaryEntry, Profile, DiaryImage, Friend

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

class DiaryEntryForm(forms.ModelForm):

    class Meta:
        model = DiaryEntry
        fields = ['title','content', 'privacy',]

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#111418] focus:outline-0 focus:ring-0 border-none bg-[#f0f2f4] focus:border-none h-14 placeholder:text-[#637588] p-4 text-base font-normal leading-normal',
            'placeholder':"Today is a beautiful day"
        })
    )

class DiaryImageForm(forms.ModelForm):
    class Meta:
        model = DiaryImage
        fields = ['image']

    # image = forms.FileField(
    #     widget=forms.FileInput(attrs={
    #         'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#111418] focus:outline-0 focus:ring-0 border-none bg-[#f0f2f4] focus:border-none h-14 placeholder:text-[#637588] p-4 text-base font-normal leading-normal',
    #     })
    # )
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']


class FriendForm(forms.ModelForm):
    # The user_from field is set to the currently logged-in user.
    user_from = forms.ModelChoiceField(queryset=User.objects.all(), initial=None, widget=forms.HiddenInput())
    user_to = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label="Select a friend")

    class Meta:
        model = Friend
        fields = ['user_from', 'user_to']

    def __init__(self, *args, **kwargs):
        # Automatically set the current user to the user_from field
        user = kwargs.pop('user')  # Extract the user argument from kwargs
        super(FriendForm, self).__init__(*args, **kwargs)
        self.fields['user_from'].initial = user  # Set initial value for 'user_from' field
        self.fields['user_from'].queryset = User.objects.filter(id=user.id)  # Limit the 'user_from' queryset to current user