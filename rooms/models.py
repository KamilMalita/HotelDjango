from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    number = models.IntegerField()
    name = models.TextField()
    price = models.IntegerField()
    description = models.TextField()


class Reservation(models.Model):
    id_customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='id_customer')
    id_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_reservation = models.IntegerField()
    end_reservation = models.IntegerField()
    id_staff = models.ForeignKey(User, on_delete=models.SET(f'{User.first_name} {User.last_name}'), blank=True, null=True, related_name='id_staff')
    price_reservation = models.IntegerField()