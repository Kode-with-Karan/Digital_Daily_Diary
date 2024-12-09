from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegisterForm, DiaryEntryForm, ProfileUpdateForm,DiaryImageForm, FriendForm
from .models import DiaryEntry, DiaryImage, Friend, User, FriendRequest,BlockedUser,CustomUser
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def add_friends(request):
    query = request.GET.get('q')
    users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query)) if query else []
    return render(request, 'friends/add_friends.html', {'users': users})

def send_friend_request(request, user_id):
    if request.method == "POST":
        to_user = get_object_or_404(User, id=user_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            messages.error(request, "Friend request already sent.")
            print("Friend request already sent.")
        else:
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            messages.success(request, "Friend request sent successfully.")
            print("Friend request sent successfully.")
    return redirect('add_friends')

def your_friends(request):
    blocked_users = BlockedUser.objects.filter(user=request.user).values_list('blocked_user', flat=True)
    friends = Friend.objects.filter(user_from=request.user).exclude(user_to__in=blocked_users)
    return render(request, 'friends/your_friends.html', {'friends': friends})

def unfollow_friend(request, user_id):
    if request.method == "POST":
        friend = get_object_or_404(User, id=user_id)
        Friend.objects.filter(user_from=request.user, user_to=friend).delete()
        Friend.objects.filter(user_from=friend, user_to=request.user).delete()
        messages.success(request, f"You have unfollowed {friend.username}.")
    return redirect('your_friends')

def friend_requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'friends/requests.html', {'requests': requests})


def accept_request(request, request_id):
    if request.method == "POST":
        friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
        Friend.objects.create(user_from=request.user, user_to=friend_request.from_user)
        Friend.objects.create(user_from=friend_request.from_user, user_to=request.user)
        friend_request.delete()  # Delete the friend request after accepting
    return redirect('friend_requests')

def decline_request(request, request_id):
    if request.method == "POST":
        friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
        friend_request.delete()  # Delete the friend request
    return redirect('friend_requests')


def suggested_friends(request):
    friends = Friend.objects.filter(user_from=request.user).values_list('user_to', flat=True)
    suggested = User.objects.exclude(id__in=friends).exclude(id=request.user.id)[:10]
    return render(request, 'friends/suggested.html', {'suggested': suggested})

def block_user(request, user_id):
    if request.method == "POST":
        to_block = get_object_or_404(User, id=user_id)
        if not BlockedUser.objects.filter(user=request.user, blocked_user=to_block).exists():
            BlockedUser.objects.create(user=request.user, blocked_user=to_block)
            Friend.objects.filter(user_from=request.user, user_to=to_block).delete()  # Remove from friends
            Friend.objects.filter(user_from=to_block, user_to=request.user).delete()  # Remove mutual friendship
            messages.success(request, f"You have blocked {to_block.username}.")
        else:
            messages.error(request, f"{to_block.username} is already blocked.")
    return redirect('your_friends')

def unblock_user(request, user_id):
    if request.method == "POST":
        blocked_user = get_object_or_404(BlockedUser, user=request.user, blocked_user_id=user_id)
        blocked_user.delete()
        messages.success(request, "User has been unblocked.")
    return redirect('blocked_friends')

def blocked_friends(request):
    blocked = BlockedUser.objects.filter(user=request.user)
    return render(request, 'friends/blocked.html', {'blocked': blocked})

def home(request):
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        con_password = request.POST.get('password2')
        
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print(username,email,password,con_password)
            CustomUser.objects.create(
                username=username,
                email=email,
                password=password , # Store plain text password
                con_password=con_password, # Store plain text password
            )
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
    entries = DiaryEntry.objects.filter(privacy__in=['public'])[::-1]
    # print(entries[0].images)
    return render(request, 'main/diary.html', {'entries': entries})

def dashboard(request):
    entries = DiaryEntry.objects.filter(user=request.user)
    return render(request, 'main/dashboard.html', {'entries': entries})

@login_required
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
    my_friends = Friend.objects.filter(user_from = request.user.id)

    friend_list = []
    for i in my_friends.exclude(id=request.user.id):
        print(i.user_to)
        friend_list.append(i.user_to)


    entries = DiaryEntry.objects.filter(user__username__in=friend_list, privacy__in=['friends','public'])[::-1]
    return render(request, 'friends/friends_update.html', {'entries':entries})


def profile_settings(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'main/profile_settings.html', {'form': form})


