from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm ,  CustomPasswordResetForm
from django.contrib.auth.models import User
from .models import Profile, Routines
from .models import Routines

# Create your views here.

def home(request):
    return render(request, "gymmy/landing.html", {})

def about(request):
    return render(request, 'gymmy/aboutpage.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome Back! {username}!')
            return redirect('homepage')
        else:
            messages.success(request,('There was an error logging in!'))
            return redirect('login')
    else:
        return render(request, 'gymmy/login.html', {})

def signup_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'gymmy/signup.html', {'form':form}) 
        

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('homepage')


@login_required
def profile_user(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        

        
        if u_form.is_valid() and p_form.is_valid() :
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile Has Been Updated!')
            return redirect('profile')

            
    else:
        u_form = UserUpdateForm(instance=request.user)
        if not hasattr(request.user, 'profile'):
            Profile.objects.create(user=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        

    context = {
        'u_form': u_form,
        'p_form': p_form,
       
    }
    return render(request, 'gymmy/profile.html', context)


def reset_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password1']

            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been successfully updated!')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'gymmy/reset_password.html', {'form': form})




def routines(request):
    query = request.GET.get('input-box')  # Get the search query from the request
    if query:
        # Filter routines that contain the search query in their name or description
        routines = Routines.objects.filter(routine__icontains=query) | Routines.objects.filter(description__icontains=query)
    else:
        # If no query, display all routines
        routines = Routines.objects.all()
    
    return render(request, 'gymmy/routines.html', {'routines': routines})

def routinedetails(request,pk):
    routinedetails = Routines.objects.get(id=pk)
    return render(request, 'gymmy/routinedetail.html', {'routinedetails':routinedetails})



