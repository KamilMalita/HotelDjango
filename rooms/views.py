from django.shortcuts import render
from django.views.generic import CreateView
from hotelapp.views import db
from django.http import HttpResponseRedirect
from .models import Room
from .forms import RoomForm

def newroom(request):
    return render(request, 'showroom.html')


def addroom(request):
    print('Im here')
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            new_room = Room(price=request.POST['price'], description=request.POST['description'], name=request.POST['name'], number=request.POST['number'])
            new_room.save()
    return HttpResponseRedirect('/room/view')


def viewRoom(request):
    rooms = Room.objects.all()
    return render(request, "showroom.html", {'all_rooms': rooms})
