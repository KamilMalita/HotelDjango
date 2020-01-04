from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='username', min_length=3, max_length=50)
    password = forms.CharField(label='password', min_length=8, max_length=50)
    password2 = forms.CharField(label='password2', min_length=8, max_length=50)
    surname = forms.CharField(label='surname', min_length=3, max_length=50)


class EditProfile(forms.Form):
    username = forms.CharField(label='username', min_length=3, max_length=50)
    email = forms.EmailField(label='email')
    name = forms.CharField(label='name', min_length=0,required=False)
    surname = forms.CharField(label='surname', min_length=3, required=False)
