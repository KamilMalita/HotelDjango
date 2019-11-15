from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


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
                user = User.objects.create_user(username, email, passw)
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
