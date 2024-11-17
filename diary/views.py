from django.shortcuts import render, redirect
from .forms import UserRegisterForm, DiaryEntryForm, ProfileUpdateForm,DiaryImageForm
from .models import DiaryEntry, DiaryImage, Friend
from django.contrib.auth import login, authenticate
from django.contrib import messages


def home(request):
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    # Redirect if the user is already logged in
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or home page after login
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'main/login.html')

def password_reset(request):
    
    
    return render(request, 'main/password_reset.html')

def diary(request):
    entries = DiaryEntry.objects.filter(user=request.user)
    return render(request, 'main/diary.html', {'entries': entries})

def dashboard(request):
    entries = DiaryEntry.objects.filter(user=request.user)
    return render(request, 'main/dashboard.html', {'entries': entries})

def create_entry(request):
    if request.method == 'POST':
        entry_form = DiaryEntryForm(request.POST)
        image_form = DiaryImageForm(request.POST, request.FILES)

        if entry_form.is_valid() and image_form.is_valid():
            # Save the diary entry first
            diary_entry = entry_form.save(commit=False)
            diary_entry.user = request.user
            diary_entry.save()

            # Save each uploaded image as a separate DiaryImage instance
            images = request.FILES.getlist('images')
            for image in images:
                DiaryImage.objects.create(diary_entry=diary_entry, image=image)

            return redirect('dashboard')
    else:
        entry_form = DiaryEntryForm()
        image_form = DiaryImageForm()

    return render(request, 'main/create_entry.html', {
        'entry_form': entry_form,
        'image_form': image_form
    })

def friends(request):
    friends = Friend.objects.filter(user_from=request.user)
    return render(request, 'main/friends.html', {'friends': friends})

def profile_settings(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'main/profile_settings.html', {'form': form})
