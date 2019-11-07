from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from .models import Room
from .forms import RoomForm


def addroom(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST' and request.POST['number'] is not '':
            same_room = Room.objects.filter(number=request.POST['number'])
            if not len(same_room):
                form = RoomForm(request.POST)
                if form.is_valid():
                    new_room = Room(price=request.POST['price'], description=request.POST['description'], name=request.POST['name'], number=request.POST['number'])
                    new_room.save()
                    return HttpResponseRedirect('/room/view')
                else:
                    rooms = Room.objects.all()
                    return render(request, "ManageRoom.html",
                                  {'err': f'{form.errors}', 'all_rooms': rooms})
            else:
                rooms = Room.objects.all()
                return render(request, "ManageRoom.html", {'msg': 'The room number is already in use.', 'all_rooms': rooms})
        else:
            print(str(request.POST))
            return redirect('/room/view')
    else:
        return HttpResponseRedirect('/')


def viewRoom(request):
    rooms = Room.objects.all()
    return render(request, "ManageRoom.html", {'all_rooms': rooms})


def deleteroom(request, room_id):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            if len(Room.objects.filter(id=room_id)):
                room_delete = Room.objects.get(id=room_id)
                room_delete.delete()
    return HttpResponseRedirect('/room/view/')


def reservation(request):
    return render(request, "Reservation.html")


def search(request):
    print('HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEJ')
    print(str(request.POST['customdate']))
    return redirect('/room/reservation')

