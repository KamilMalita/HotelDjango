from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def home_request(request):
    return render(request, 'Home.html')


def register_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('pass')
        try:
            user = User.objects.create_user(email, email, passw)
            user.date_joined = datetime.datetime.now()
            user.save()
        except:
            message = "Invalid credentials"
            return render(request, "Register.html", {"msg": message})
        return render(request, "Home.html")
    else:
        return render(request, "Register.html")


def login_request(request):
    if request.method == 'POST':
        # form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid():
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "Home.html", {"e": 'hejo hejo'})
        else:
            return render(request, "Login.html", {"e": request.user})
        message = "Invalid credentials"
        return render(request, "Login.html", {"msg": message})
    print('No POST')
    return render(request, "Login.html")


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "Home.html")