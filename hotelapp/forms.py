from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='username', min_length=5, max_length=50)
    password = forms.CharField(label='password', min_length=8, max_length=50)
    password2 = forms.CharField(label='password2', min_length=8, max_length=50)