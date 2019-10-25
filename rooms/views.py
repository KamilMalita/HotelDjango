from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from .models import Room
from .forms import RoomForm


def addroom(request):
    same_room = Room.objects.filter(number=request.POST['number'])
    if not len(same_room):
        if request.method == 'POST':
            print(request.POST)
            form = RoomForm(request.POST)
            if form.is_valid():
                new_room = Room(price=request.POST['price'], description=request.POST['description'], name=request.POST['name'], number=request.POST['number'])
                new_room.save()
        return HttpResponseRedirect('/room/view')
    else:
        rooms = Room.objects.all()
        return render(request, "AddRoom.html", {'msg': 'The room number is already in use.', 'all_rooms': rooms})


def viewRoom(request):
    rooms = Room.objects.all()
    return render(request, "AddRoom.html", {'all_rooms': rooms})



