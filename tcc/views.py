
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    return render(request, "tcc/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        passwd = request.POST['password']

        if User.objects.filter(username=username):
            return render(request, "tcc/signup.html", {"error":"Este username já está em uso. Por favor escolha outro."})

        if User.objects.filter(email=email):
            return render(request, "tcc/signup.html", {"error":"Este email já está em uso. Por favor escolha outro."})

        if len(username) > 20:
            return render(request, "tcc/signup.html", {"error":"O Username não pode ter mais de 20 caracteres."})

        if len(passwd) < 6:
            return render(request, "tcc/signup.html", {"error":"A senha precisa ter no mínimo 6 caracteres."})
        
        newuser = User.objects.create_user(username, email, passwd)
        newuser.save()
        messages.success(request, "Account created.")
        return redirect('signin')
    return render(request, "tcc/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(username=username, password=passwd)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "tcc/signin.html", {"error":"Credenciais erradas."})
    return render(request, "tcc/signin.html")

def signout(request):
    logout(request)
    return redirect("home")