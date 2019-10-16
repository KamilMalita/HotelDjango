from django.shortcuts import render
import pyrebase

config = {
    'apiKey': "AIzaSyCr-FHDGQVkUcfG3VdQTykjHaVaMtTwiA4",
    'authDomain': "baza-hotelowa.firebaseapp.com",
    'databaseURL': "https://baza-hotelowa.firebaseio.com",
    'projectId': "baza-hotelowa",
    'storageBucket': "baza-hotelowa.appspot.com",
    'messagingSenderId': "1064584579921",
    'appId': "1:1064584579921:web:a934e59fbc812ec2"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


def signIN(request):
    return render(request, "SignIn.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid credentials"
        return render(request, "SignIn.html", {"msg": message})
    print(user['idToken'])
    return render(request, "Welcome.html", {"e": email})