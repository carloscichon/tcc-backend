import base64
from PIL import Image
import binascii
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room
from .classification import process_image
# Create your views here.

@login_required
def rooms(request):
    rooms = Room.objects.filter(owner=request.user)
    return render(request, 'room/rooms.html', {'rooms': rooms})


def room(request, slug):
    room = Room.objects.get(slug=slug)
    if request.user == room.owner:
        return render(request, 'room/roomowner.html', {'room': room})
    if request.method == "POST":
        passwd = request.POST['rpasswd']
        if passwd == room.passwd:
            room.active_members = room.active_members + 1
            room.save()
            return render(request, 'room/room.html', {'room': room})
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
        room.active_members = room.active_members - 1
        room.save()
        #print("alguem saiu")
        return redirect('home')
   
def image(request, slug):
    if request.method == "POST":
        base_image = request.POST['baseImage']
        base_image_cut = base_image[22:]
        try:
            img = base64.b64decode(base_image_cut)
        except binascii.Error as error:
            print(error)
            
        #with open("teste.png", "wb+") as file:
        #    file.write(img)
        process_image(img)
        return HttpResponse("Image received.")
