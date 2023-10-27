from django.db import models
from django.contrib.auth.models import User


class State(models.IntegerChoices):
    OFFLINE = 0, 'Offline'
    WAITING = 1, 'Waiting'
    STARTED = 2, 'Started'

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    passwd = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    active_members = models.IntegerField(default=0)
    state = models.IntegerField(default=State.OFFLINE, choices=State.choices)

class Moment(models.Model):
    time = models.IntegerField(default=0)
    expression = models.CharField(max_length=255)
    id_inroom = models.IntegerField(default=0)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
