from django.db import models


class Room(models.Model):
    number = models.IntegerField()
    name = models.TextField()
    price = models.IntegerField()
    description = models.TextField()


