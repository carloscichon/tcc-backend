import base64
from PIL import Image
import binascii
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room, Moment, State
from .classification import process_image, teste
# Create your views here.

@login_required
def rooms(request):
    rooms = Room.objects.filter(owner=request.user)
    return render(request, 'room/rooms.html', {'rooms': rooms})


def room(request, slug):
    room = Room.objects.get(slug=slug)
    if request.user == room.owner:
        #if room.state == State.OFFLINE:
        Moment.objects.filter(room=room).delete()
        room.state = State.WAITING
        room.save()
        return render(request, 'room/roomowner.html', {'room': room})
    if request.method == "POST":
        passwd = request.POST['rpasswd']
        if passwd == room.passwd:
            room.active_members = room.active_members + 1
            room.save()
            return render(request, 'room/room.html', {'room': room, 'room_id': room.active_members})
        return render(request, 'room/roompass.html', {'room': room, 'error': "Wrong password"})
    return render(request, 'room/roompass.html', {'room': room})
    
@login_required
def new(request):
    if request.method == "POST":
        print("aaa")
        user = request.user
        rname = request.POST['rname']
        rcode = request.POST['rcode']
        rpasswd = request.POST['rpasswd']
        if Room.objects.filter(slug=rcode):
            return render(request, "room/newroom.html", {"error":"Room code already exists. Please try some other code."})
        if len(rname) > 50:
            return render(request, "room/newroom.html", {"error": "Room name can not be than 50 characters."})
        if len(rpasswd) < 6:
            return render(request, "room/newroom.html", {"error": "Password needs to be at least 6 characters long."})
        newroom = Room.objects.create(name=rname, slug=rcode, passwd=rpasswd, owner=user)
        newroom.save()
        return redirect('rooms')

    return render(request, "room/newroom.html")

def leave(request, slug):
    if request.method == "POST":
        room = Room.objects.get(slug = slug)
        if request.user == room.owner:
            room.active_members = 0
            room.state = State.OFFLINE
            room.save()
            Moment.objects.filter(room=room).delete()
            return redirect('home')
        room.active_members = room.active_members - 1
        room.save()
        #print("alguem saiu")
        return redirect('home')
   
def image(request, slug):
    #print(slug)
    if request.method == "POST":
        base_image = request.POST['baseImage']
        base_image_cut = base_image[22:]
        moment = int(request.POST['moment'])
        in_room = int(request.POST['in_room'])
        actual_room = Room.objects.get(slug=slug)
        if actual_room.state == State.STARTED:
            try:
                img = base64.b64decode(base_image_cut)
                expression = process_image(img)
                #print(expression)
                if expression:
                    newMoment = Moment.objects.create(time=moment, expression=expression, id_inroom=in_room, room=actual_room)
                    newMoment.save()
                    return HttpResponse("Image received.")
                return HttpResponse("No expression found in the image.")
            except binascii.Error as error:
                print(error)
                return HttpResponse("Could not decode.")
        else:
            return HttpResponse("Room is not started.")
    
@login_required
def start(request, slug):
    room = Room.objects.get(slug=slug)
    if request.method == "POST" and request.user == room.owner:
        room.state = State.STARTED
        room.save()
        return HttpResponse("Room started.")
    return HttpResponse("Could not start.")
