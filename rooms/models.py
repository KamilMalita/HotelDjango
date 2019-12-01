from django.db import models
from django.contrib.auth.models import User


class RoomType(models.Model):
    name = models.TextField(max_length=100)
    capacityAdults = models.IntegerField()
    capacityKids = models.IntegerField()
    marriage = models.BooleanField(default=False)
    apartment = models.BooleanField(default=False)
    multiplier = models.FloatField()


class Room(models.Model):
    number = models.IntegerField()
    name = models.TextField()
    price = models.IntegerField()
    description = models.TextField()
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)


class Reservation(models.Model):
    id_customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='id_customer')
    id_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_reservation = models.IntegerField()
    end_reservation = models.IntegerField()
    id_staff = models.ForeignKey(User, on_delete=models.SET(f'{User.first_name} {User.last_name}'), blank=True, null=True, related_name='id_staff')
    price_reservation = models.IntegerField()
