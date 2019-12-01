from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from .models import Room, Reservation, RoomType
from .forms import RoomForm, TypeForm
import datetime


def addroom(request):
    print(request.POST)
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST' and request.POST['number'] is not '':
            same_room = Room.objects.filter(number=request.POST['number'])
            if not len(same_room):
                form = RoomForm(request.POST)
                if form.is_valid():
                    type_id = RoomType.objects.filter(name=request.POST['type'])
                    new_room = Room(price=request.POST['price'], description=request.POST['description'],
                                    name=request.POST['name'], number=request.POST['number'],
                                    type_id=type_id[0].id)
                    new_room.save()
                    return HttpResponseRedirect('/room/view')
                else:
                    rooms = Room.objects.all().order_by('number')
                    types = RoomType.objects.all().order_by('name')
                    return render(request, "ManageRoom.html",
                                  {'err': f'{form.errors}', 'all_rooms': rooms, 'all_types': types})
            else:
                rooms = Room.objects.all().order_by('number')
                types = RoomType.objects.all().order_by('name')
                return render(request, "ManageRoom.html",
                              {'msg': 'The room number is already in use.', 'all_rooms': rooms, 'all_types': types})
        else:
            print(str(request.POST))
            return redirect('/room/view')
    else:
        return HttpResponseRedirect('/')


def viewRoom(request):
    rooms = Room.objects.all().order_by('number')
    types = RoomType.objects.all().order_by('name')
    print(types)
    return render(request, "ManageRoom.html", {'all_rooms': rooms, 'all_types': types})


def deleteroom(request, room_id):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            if len(Room.objects.filter(id=room_id)):
                room_delete = Room.objects.get(id=room_id)
                room_delete.delete()
    return HttpResponseRedirect('/room/view/')


def editroomquery(request, room_id):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'GET':
            if len(Room.objects.filter(id=room_id)):
                types = RoomType.objects.all().order_by('name')
                return render(request, "EditRoom.html", {'RoomEdit': Room.objects.get(id=room_id), 'all_types': types})
        elif request.method == "POST":
            print(request.POST)
            if len(Room.objects.filter(id=room_id)):
                type_id = RoomType.objects.filter(name=request.POST['type'])
                room_edit = Room.objects.filter(id=room_id).update(name=request.POST['name'],
                                                                   price=request.POST['price'],
                                                                   number=request.POST['number'],
                                                                   description=request.POST['description'],
                                                                   type_id=type_id[0].id)
    return HttpResponseRedirect('/room/view/')


def edittypequery(request, type_id):
    updatemsg = ''
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'GET':
            if len(RoomType.objects.filter(id=type_id)):
                return render(request, "EditType.html", {'TypeEdit': RoomType.objects.get(id=type_id)})
        elif request.method == "POST":
            print(request.POST)
            if len(RoomType.objects.filter(id=type_id)):
                form = TypeForm(request.POST)
                if form.is_valid():
                    apartment = 'False'
                    marriage = 'False'
                    if request.POST['apartment'] == 'on':
                        apartment = 'True'
                    if request.POST['marriage'] == 'on':
                        marriage = 'True'
                    old_multiplier = RoomType.objects.get(id=type_id).multiplier
                    type_edit = RoomType.objects.filter(id=type_id).update(name=request.POST['name'], marriage=marriage,
                                        multiplier=request.POST['multiplier'], apartment=apartment,
                                        capacityKids=request.POST['capacityKids'],
                                        capacityAdults=request.POST['capacityAdults'])
                    rooms = Room.objects.filter(type_id=type_id)
                    for room in rooms:
                        Room.objects.filter(id=room.id).update(price=int(room.price/old_multiplier*float(request.POST['multiplier'])))
                    updatemsg = f'Successfully update {request.POST["name"]} room.'
                    types = RoomType.objects.all().order_by('name')
                    return render(request, 'TypesRoom.html', {'updatemsg': updatemsg, 'all_rooms': types})
                else:
                    return render(request, "EditType.html", {'TypeEdit': RoomType.objects.get(id=type_id), 'err': form.errors})
    return HttpResponseRedirect('/room/types/')


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
        all_reservations = Reservation.objects.all().filter(id_customer_id=request.user.id).order_by(
            'start_reservation')
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
            busy_room = int(len(rooms)) - int(len(free_rooms))
            return render(request, "HotelOccupancy.html",
                          {'busy_rooms': busy_room, 'all_rooms': len(rooms), 'free_rooms': len(free_rooms)})
        return render(request, "HotelOccupancy.html")
    return render(request, "Home.html")


def types_room(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST' and request.POST['name'] is not '':
            same_room = RoomType.objects.filter(name=request.POST['name'])
            if not len(same_room):
                form = TypeForm(request.POST)
                if form.is_valid():
                    apartment = 'False'
                    marriage = 'False'
                    if request.POST['apartment'] == 'on':
                        apartment = 'True'
                    if request.POST['marriage'] == 'on':
                        marriage = 'True'
                    new_type = RoomType(name=request.POST['name'], marriage=marriage,
                                        multiplier=request.POST['multiplier'], apartment=apartment,
                                        capacityKids=request.POST['capacityKids'],
                                        capacityAdults=request.POST['capacityAdults'])
                    new_type.save()
                types = RoomType.objects.all().order_by('name')
                return render(request, "TypesRoom.html",
                              {'err': f'{form.errors}', 'all_rooms': types})
            else:
                types = RoomType.objects.all().order_by('name')
                return render(request, "TypesRoom.html",
                              {'msg': 'The name of type is already in use', 'all_rooms': types})
        types = RoomType.objects.all().order_by('name')
        return render(request, "TypesRoom.html", {'all_rooms': types})
    return redirect('/')


def deletetype(request, type_id):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            if len(RoomType.objects.filter(id=type_id)):
                room_delete = RoomType.objects.get(id=type_id)
                room_delete.delete()
    return HttpResponseRedirect('/room/types/')
