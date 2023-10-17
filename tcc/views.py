from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "tcc/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        passwd = request.POST['password']
        newuser = User.objects.create_user(username, email, passwd)
        newuser.save()
        messages.success(request, "Account created.")
        return redirect('signin')
    return render(request, "tcc/signup.html")

def signin(request):
    return render(request, "tcc/signin.html")

def signout(request):
    pass