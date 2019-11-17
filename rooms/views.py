from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from .models import Room, Reservation
from .forms import RoomForm
import datetime


def addroom(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST' and request.POST['number'] is not '':
            same_room = Room.objects.filter(number=request.POST['number'])
            if not len(same_room):
                form = RoomForm(request.POST)
                if form.is_valid():
                    new_room = Room(price=request.POST['price'], description=request.POST['description'],
                                    name=request.POST['name'], number=request.POST['number'])
                    new_room.save()
                    return HttpResponseRedirect('/room/view')
                else:
                    rooms = Room.objects.all().order_by('number')
                    return render(request, "ManageRoom.html",
                                  {'err': f'{form.errors}', 'all_rooms': rooms})
            else:
                rooms = Room.objects.all().order_by('number')
                return render(request, "ManageRoom.html",
                              {'msg': 'The room number is already in use.', 'all_rooms': rooms})
        else:
            print(str(request.POST))
            return redirect('/room/view')
    else:
        return HttpResponseRedirect('/')


def viewRoom(request):
    rooms = Room.objects.all().order_by('number')
    return render(request, "ManageRoom.html", {'all_rooms': rooms})


def deleteroom(request, room_id):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            if len(Room.objects.filter(id=room_id)):
                room_delete = Room.objects.get(id=room_id)
                room_delete.delete()
    return HttpResponseRedirect('/room/view/')


def reservation(request):
    if request.user.is_authenticated and request.method == 'POST':
        date_all = request.POST['customdate']
        date_start = str(date_all).split(':')[0]
        date_end = str(date_all).split(':')[1]
        list_busy_rooms = Reservation.objects.filter(start_reservation__lt=date_end.replace('-', '')).filter(
            end_reservation__gt=date_start.replace('-', ''))
        tab_exclude = []
        for liss in list_busy_rooms:
            tab_exclude.append(liss.id_room.number)  # define busy rooms in this date
        try:
            x = request.POST['myCheck']
            rooms = Room.objects.all().exclude(number__in=tab_exclude)
        except:
            if request.POST['price_min'] > request.POST['price_max']:
                return render(request, "SearchRooms.html", {'price_err': "Minimum price can not be lower than maximum"})
            rooms = Room.objects.all().filter(price__gte=request.POST['price_min']).filter(
                price__lte=request.POST['price_max']).exclude(number__in=tab_exclude)
        print(len(rooms))
        days = int(date_end.replace('-', '')) - int(date_start.replace('-', ''))
        if len(rooms):
            return render(request, "Reservation.html",
                          {'length': days, 'free_rooms': rooms, 'start_date': date_start, 'end_date': date_end})
        else:
            return render(request, "SearchRooms.html", {'err': "No free rooms in this date"})
    return redirect('/')


def search(request):
    if request.user.is_authenticated:
        return render(request, "SearchRooms.html")
    else:
        return redirect('/')


def reservation_create(request):
    if request.method == 'POST' and request.user.is_authenticated:
        print(request.POST)
        start_date = str(request.POST['start_date']).replace('-', '')
        end_date = str(request.POST['end_date']).replace('-', '')
        room_id = request.POST['room_id']
        price = request.POST['price']
        user = request.user.id
        try:
            if request.user.is_superuser or request.user.is_staff:
                create_reservation = Reservation.objects.create(start_reservation=start_date, end_reservation=end_date,
                                                                price_reservation=price, id_room_id=room_id,
                                                                id_customer_id=user, id_staff_id=user)
            else:
                create_reservation = Reservation.objects.create(start_reservation=start_date, end_reservation=end_date,
                                                                price_reservation=price, id_room_id=room_id,
                                                                id_customer_id=user)
            create_reservation.save()
        except Exception as e:
            print(e)
        return HttpResponse('<h1>Page was found</h1>')
    return redirect('/')


def my_reservations(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            all_reservations = Reservation.objects.all().order_by('start_reservation')
            return render(request, "MyReservations.html", {'all_reservations': all_reservations})
        all_reservations = Reservation.objects.all().filter(id_customer_id=request.user.id).order_by('start_reservation')
        return render(request, "MyReservations.html", {'all_reservations': all_reservations})
    return render(request, "Home.html")


def hotel_occupancy(request):
    """"Documentation for a function.
    This function returns fundamentals info about occupancy of Hotel.
    """
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            date_all = request.POST['occupancy_date']
            date_start = str(date_all).split(':')[0]
            date_end = str(date_all).split(':')[1]
            list_busy_rooms = Reservation.objects.filter(start_reservation__lt=date_end.replace('-', '')).filter(
                end_reservation__gt=date_start.replace('-', ''))
            tab_exclude = []
            for liss in list_busy_rooms:
                tab_exclude.append(liss.id_room.number)
            rooms = Room.objects.all()
            free_rooms = rooms.exclude(number__in=tab_exclude)
            busy_room = int(len(rooms))-int(len(free_rooms))
            return render(request, "HotelOccupancy.html", {'busy_rooms': busy_room, 'all_rooms': len(rooms), 'free_rooms': len(free_rooms)})
        return render(request, "HotelOccupancy.html")
    return render(request, "Home.html")