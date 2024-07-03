from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.forms import LoginForm, UserRegistrationForm
from .models import Profile

from .forms import UserEditForm, ProfileEditForm
from posts.models import Post

# Create your views here.
def user_login(request):
    if request.POST:
        form = LoginForm(request.POST)  
                                                 #get the data(username, password) from the request
        if form.is_valid():                                                       #django inbuild function to check if form is valid or not
            data = form.cleaned_data                                                #now clean the data and save it in data
            user = authenticate(request, username = data['username'], 
                                password = data['password'])                        #authenticate checks the username and password in the database, returns the user object if it is present 
            if user is not None:
                login(request, user)                                                #login method -->user object is passed
                return HttpResponse("User authenticated and logged in")
            else:
                return HttpResponse("Invalid Credentials")
    else:
        form = LoginForm() 
    return render(request, 'users/login.html', {'form': form})



# The @login_required decorator in Django is used to ensure
#  that a view can only be accessed by authenticated users.
#  When a user who is not authenticated tries to access a 
# view decorated with @login_required, they will be 
# redirected to the login page.


# By default, the @login_required decorator will 
# redirect unauthenticated users to the URL specified by 
# the LOGIN_URL setting in your Django settings file. 
# You can customize this URL by either setting LOGIN_URL 
# in your settings or by passing the login_url parameter 
# to the decorator.
@login_required(login_url='login')
def index(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user)
    profile = Profile.objects.filter(user =current_user).first()
    return render(request, 'users/index.html', {'posts': posts, 'profile':profile})

def user_logout(request):
    logout(request)
    return render(request, 'users/logout.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False) #commit=False means we are saving everything except password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user = new_user)  #after registering user, we will update profile
            return render(request, 'users/register_done.html')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user, data=request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)

    return render(request, 'users/edit.html', {'user_form': user_form, 'profile_form': profile_form})




