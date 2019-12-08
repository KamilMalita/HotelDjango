from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, EditProfile


def home_request(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'Home.html')


def register_request(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            passw = request.POST.get('password')
            passw2 = request.POST.get('password2')
            if passw != passw2:
                message = 'Passwords mus be the same'
                return render(request, "Register.html", {"msg": message})
            try:
                user = User.objects.create_user(username=username, email=email, password=passw,
                                                first_name=request.POST['name'],
                                                last_name=request.POST['surname'])
                user.date_joined = datetime.datetime.now()
                user.save()
            except:
                message = "Username is busy"
                return render(request, "Register.html", {"error_username": message})
            return render(request, "Home.html")
        else:
            message = str(form.errors)
            return render(request, "Register.html", {"msg": message})
    else:
        return render(request, "Register.html")


def login_request(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, "Login.html", {"msg": 'Invalid username or password'})
        return render(request, "Login.html")
    else:
        return redirect('/')


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "Home.html")


def profile(request):
    if request.method == 'POST':
        print(request.POST)
        form = EditProfile(request.POST)
        if form.is_valid():
            edit_user = User.objects.filter(username=request.user.username).update(email=request.POST['email'],
                                                                                   first_name=request.POST['name'],
                                                                                   last_name=request.POST['surname'])
        else:
            user = User.objects.get(username=request.user.username)
            return render(request, "Profile.html", {'User': user, 'error_email': 'Invalid email address'})
        user = User.objects.get(username=request.user.username)
        return render(request, "Profile.html", {'User': user})
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        return render(request, "Profile.html", {'User': user})
    return render(request, "Home.html")


def changepass(request):
    if request.user.is_authenticated and request.method == 'POST':
        error_pass = ''
        form = RegisterForm(request.POST)
        if form.is_valid():
            if request.POST['password'] == request.POST['password2']:
                print(request.POST)
                if request.user.check_password(request.POST['password2']):
                    print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')
                # user = User.objects.get(username=request.user.username).set_password()
            else:
                error_pass = 'Passwords must be the same'
        else:
            error_pass = "Passwords must be longer than 8 characters"
        user = User.objects.get(username=request.user.username)
        return render(request, "Profile.html", {"User": user, "error_pass": error_pass})
    return render(request, "Home.html")
