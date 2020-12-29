from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        return render(request, "mariage/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))


def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Not logged in")

    else:
        return render(request, "mariage/login.html")


def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        print("method is post")
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            print("Passwords do not match")
            return render(request, "mariage/register.html", {
                "message": "Provided passwords do not match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            print("Username is already taken.")
            return render(request, "mariage/register.html", {
                "message": "Username is already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mariage/register.html")
