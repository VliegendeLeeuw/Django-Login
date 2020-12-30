from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import UserRegistration


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
            messages.success(request, 'Succesfully logged in.')
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'Login failed.')
            return HttpResponse("Not logged in")

    else:
        return render(request, "mariage/login.html")


def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    form = UserRegistration()
    if request.method == "POST":
        print("method is post")
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, 'Provided passwords do not match.')
            return HttpResponseRedirect(reverse("register"))
        try:
            user = User.objects.create_user(username, email, password)
            user.last_name = last_name
            user.first_name = first_name
            user.save()
        except IntegrityError:
            messages.error(request, 'Username is already taken.')
            return render(request, "mariage/register.html")
        login(request, user)
        messages.success(request, 'Succesfully registered new account.')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mariage/register.html", {
            'form': form,
        })
