from django.shortcuts import render, redirect
from .forms import UserRegisterForm, DiaryEntryForm, ProfileUpdateForm,DiaryImageForm, FriendForm
from .models import DiaryEntry, DiaryImage, Friend, User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    entries = DiaryEntry.objects.all()[::-1]
    # print(entries[0].images)
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
            images = request.FILES.getlist('image')
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




@login_required
def friends_follow(request):
    if request.method == 'POST':
        form = FriendForm(request.POST, user=request.user)  # Pass the logged-in user
        if form.is_valid():
            # Create the friendship in both directions
            
            if(request.POST['opt'] == "follow"):
                friend = form.save(commit=False)
                friend.user_from = request.user  # Ensure the logged-in user is user_from
                friend.save()

                # Optionally, create the reverse friendship (user_to adds user_from)
                Friend.objects.create(user_from=form.cleaned_data['user_to'], user_to=request.user)

                return redirect('friends_follow')  # Redirect to a friends list page or wherever you want
            elif(request.POST['opt'] == "delete"):

                friend = Friend.objects.get(user_from=request.user, user_to_id=form.cleaned_data['user_to'])
                reverse_friend = Friend.objects.get(user_from=form.cleaned_data['user_to'], user_to=request.user)

                # Delete both directions of the friendship
                friend.delete()
                reverse_friend.delete()

                # Redirect back to the friends list after deleting
                return redirect('friends_follow')
    
            
    else:
        form = FriendForm(user=request.user)
    # print(request.user)
    friends = User.objects.all()
    my_friends = Friend.objects.filter(user_from = request.user.id)
    # print(my_friends.values('user_to'))
    friends_to_display = friends.exclude(id__in=my_friends.values('user_to')).exclude(id=request.user.id)

    entries = DiaryEntry.objects.filter(user__username__in=[ "karan", "Peehu@kusi"])[::-1]
    return render(request, 'main/friends_follow.html', {'friends': friends_to_display, 'entries':entries, 'form': form, 'my_friends':my_friends})


@login_required
def friends_unfollow(request):
    if request.method == 'POST':
        form = FriendForm(request.POST, user=request.user)  # Pass the logged-in user
        if form.is_valid():
            # Create the friendship in both directions
            
            if(request.POST['opt'] == "follow"):
                friend = form.save(commit=False)
                friend.user_from = request.user  # Ensure the logged-in user is user_from
                friend.save()

                # Optionally, create the reverse friendship (user_to adds user_from)
                Friend.objects.create(user_from=form.cleaned_data['user_to'], user_to=request.user)

                return redirect('friends_unfollow')  # Redirect to a friends list page or wherever you want
            elif(request.POST['opt'] == "delete"):

                friend = Friend.objects.get(user_from=request.user, user_to_id=form.cleaned_data['user_to'])
                reverse_friend = Friend.objects.get(user_from=form.cleaned_data['user_to'], user_to=request.user)

                # Delete both directions of the friendship
                friend.delete()
                reverse_friend.delete()

                # Redirect back to the friends list after deleting
                return redirect('friends_unfollow')
    
            
    else:
        form = FriendForm(user=request.user)
    # print(request.user)
    friends = User.objects.all()
    my_friends = Friend.objects.filter(user_from = request.user.id)
    # print(my_friends.values('user_to'))
    friends_to_display = friends.exclude(id__in=my_friends.values('user_to')).exclude(id=request.user.id)

    entries = DiaryEntry.objects.filter(user__username__in=[ "karan", "Peehu@kusi"])[::-1]
    return render(request, 'main/friends_unfollow.html', {'friends': friends_to_display, 'entries':entries, 'form': form, 'my_friends':my_friends})


@login_required
def friends(request):

    if request.method == 'POST':
        form = FriendForm(request.POST, user=request.user)  # Pass the logged-in user
        if form.is_valid():
            # Create the friendship in both directions
            
            if(request.POST['opt'] == "follow"):
                friend = form.save(commit=False)
                friend.user_from = request.user  # Ensure the logged-in user is user_from
                friend.save()

                # Optionally, create the reverse friendship (user_to adds user_from)
                Friend.objects.create(user_from=form.cleaned_data['user_to'], user_to=request.user)

                return redirect('friends')  # Redirect to a friends list page or wherever you want
            elif(request.POST['opt'] == "delete"):

                friend = Friend.objects.get(user_from=request.user, user_to_id=form.cleaned_data['user_to'])
                reverse_friend = Friend.objects.get(user_from=form.cleaned_data['user_to'], user_to=request.user)

                # Delete both directions of the friendship
                friend.delete()
                reverse_friend.delete()

                # Redirect back to the friends list after deleting
                return redirect('friends')
    
            
    else:
        form = FriendForm(user=request.user)
    # print(request.user)
    friends = User.objects.all()
    my_friends = Friend.objects.filter(user_from = request.user.id)
    # print(my_friends.values('user_to'))
    friends_to_display = friends.exclude(id__in=my_friends.values('user_to')).exclude(id=request.user.id)

    entries = DiaryEntry.objects.filter(user__username__in=[ "karan", "Peehu@kusi"])[::-1]
    return render(request, 'main/friends_update.html', {'friends': friends_to_display, 'entries':entries, 'form': form, 'my_friends':my_friends})

def profile_settings(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'main/profile_settings.html', {'form': form})


# @login_required
# def add_friend(request):
#     if request.method == 'POST':
#         form = FriendForm(request.POST, user=request.user)  # Pass the logged-in user
#         if form.is_valid():
#             # Create the friendship in both directions
#             friend = form.save(commit=False)
#             friend.user_from = request.user  # Ensure the logged-in user is user_from
#             friend.save()

#             # Optionally, create the reverse friendship (user_to adds user_from)
#             Friend.objects.create(user_from=form.cleaned_data['user_to'], user_to=request.user)

#             return redirect('friends')  # Redirect to a friends list page or wherever you want
#     else:
#         form = FriendForm(user=request.user)

#     return render(request, 'friends/add_friend.html', {'form': form})