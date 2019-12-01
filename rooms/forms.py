from django import forms


class RoomForm(forms.Form):
    name = forms.CharField(label='name', max_length=60, min_length=5)
    price = forms.IntegerField(label='price', max_value=2000, min_value=10)
    description = forms.CharField(label='Description', max_length=1000, min_length=2)
    number = forms.IntegerField(label='number', max_value=499, min_value=1)
    type = forms.CharField(label='type')


class TypeForm(forms.Form):
    name = forms.CharField(label='name', max_length=60, min_length=3)
    multiplier = forms.FloatField(label='multiplier', max_value=30, min_value=1.0)
    marriage = forms.BooleanField(label='marriage', initial=False)
    apartment = forms.BooleanField(label='apartment', initial=False)
    capacityAdults = forms.IntegerField(label='capacityAdults', max_value=10, min_value=0)
    capacityKids = forms.IntegerField(label='capacityKids', max_value=10, min_value=0)

