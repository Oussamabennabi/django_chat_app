from django.shortcuts import render, redirect
from django.db.models.query import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# modles :
from .models import Room, Topic

#  forms
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("Home")
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Invalid password')
    context = {}
    return render(request, 'base/login_user.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # this is if we want to change the user infos
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("Home")
        else:
            messages.error(request,"an error occured during registration")
    context = {'form': form}
    return render(request, 'base/register_user.html', context)


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q))
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def room(request, id):
    room = Room.objects.get(id=id)
    if (room == None):
        return HttpResponse("there is no room with such id!!")
    return render(request, 'base/room.html', {'room': room})


@login_required(login_url='login')
def createRoom(request):
    print("entered createRoom")
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, roomId):
    room = Room.objects.get(id=roomId)
    if (request.user != room.host):
        messages.error(request, "you are not allowed here!")

    if (room == None):
        return redirect('Home')
    form = RoomForm(instance=room)
    if request.method == 'POST':
        # you nedd to tell it which room to update
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, roomId):
    room = Room.objects.get(id=roomId)

    if (request.user != room.host):
        messages.error(request, "you are not allowed here!")

    if room == None:
        return redirect("Home")
    if (request.method == 'POST'):
        room.delete()
        return redirect("Home")
    return render(request, 'base/delete.html', {'obj': room})
