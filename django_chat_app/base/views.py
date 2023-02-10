from django.shortcuts import render, redirect
from django.db.models.query import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# modles :
from .models import Room, Topic, Message, User


#  forms
from .forms import RoomForm, UserUpdateForm, UserCreate


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("Home")
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, email=email, password=password)
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
    form = UserCreate()
    if request.method == 'POST':
        form = UserCreate(request.POST,request.FILES)
        if form.is_valid():
            # this is if we want to change the user infos
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("Home")
        else:
            messages.error(request, "an error occured during registration")
    context = {'form': form}
    return render(request, 'base/register_user.html', context)


# @login_required(login_url='login')
def home(request):
    if request.user.is_active :
        print("Is Online")
    q = request.GET.get('q') if request.GET.get('q') else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q))
    topics = Topic.objects.all()[0:6]

    rooms_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)).order_by('-updated_at', '-created_at')
    activity_messages = room_messages[0:4]
    context = {'rooms': rooms, 'topics': topics,
               'room_messages': room_messages, 'rooms_count': rooms_count, 'activity_messages': activity_messages}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def room(request, id):

    room = Room.objects.get(id=id)
    topics = Topic.objects.all()
    room_messages = room.message_set.all()
    participants = room.participants.all()
    participants_count = participants.count()
    if request.method == 'POST':
        message = request.POST.get('message')
        Message.objects.create(body=message, user=request.user, room=room)
        room.participants.add(request.user)
    if (room == None):

        return HttpResponse("there is no room with such id!!")
    context = {'room': room, 'room_messages': room_messages, 'topics': topics,
               'participants': participants, 'participants_count': participants_count}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            name=request.POST.get(
            'name'),
            topic =topic,
            description=request.POST.get(
            'description')
            )
        
        return redirect('Home')

    typeOfRequest = 'create'

    topics = Topic.objects.all()
    # topics
    context = {'form': form, 'typeOfRequest': typeOfRequest, 'topics': topics}
    return render(request, 'base/create_room.html', context)


@login_required(login_url='login')
def updateRoom(request, roomId):
    room = Room.objects.get(id=roomId)
    if (request.user != room.host):
        messages.error(request, "you are not allowed here!")

    if (room is None):
        return redirect('Home')
    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('Home')
    typeOfRequest = 'update'
    topics = Topic.objects.all()
    context = {'form': form, 'typeOfRequest': typeOfRequest, 'topics': topics,'room':room}
    return render(request, 'base/create_room.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteMessage(request, messageId):
    message = Message.objects.get(id=messageId)

    if (request.user != message.user):
        messages.error(request, "you cant delete others messages!")

    if message == None:
        return redirect("Home")
    if (request.method == 'POST'):
        message.delete()
        return redirect("Home")
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def userProfile(request, userId):
    user = User.objects.get(id=userId)
    rooms = user.room_set.all()
    topics = Topic.objects.all()[0:6]
    activity_messages = Message.objects.filter(Q(user=user))[0:4]
    context = {'user': user, 'rooms': rooms,
               'topics': topics, 'activity_messages': activity_messages}
    return render(request, 'base/user_profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    rooms = Room.objects.filter(host=user)
    form = UserUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',userId=user.id)
    context = {'user': user, 'rooms': rooms,'form': form}
    return render(request,'base/update_user.html',context)



def activityPage(requset):
    activity_messages = Message.objects.all().order_by('-updated_at', '-created_at')
    return render(requset,'base/activity_page.html',{"activity_messages":activity_messages})


def topicsPage(request,):
    q = request.GET.get('q') if request.GET.get('q') else ''

    topics = Topic.objects.filter(Q(name__icontains=q))
    return render(request,'base/topics_page.html',{"topics":topics})
