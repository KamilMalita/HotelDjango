from django import forms


class RoomForm(forms.Form):
    name = forms.CharField(label='Whatever', max_length=60, min_length=5)
    price = forms.IntegerField(label='0', max_value=2000, min_value=10)
    description = forms.CharField(label='Description', max_length=1000, min_length=2)
    number = forms.IntegerField(label='0', max_value=499, min_value=1)
