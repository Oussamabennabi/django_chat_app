from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='Home'),
    path("activities/", views.activityPage, name='activities'),
    path("topics/", views.topicsPage, name='topics'),
    

    path("login/", views.loginUser, name='login'),
    path("user-profile/<str:userId>", views.userProfile, name='user-profile'),
    path("settings/", views.updateUser, name='settings'),
    path("logout/", views.logoutUser, name='logout'),
    path("register/", views.registerUser, name='register'),
 
    path("room/<str:id>", views.room, name='room'),
    path("create-room/", views.createRoom, name='create-room'),
    path("update-room/<str:roomId>/", views.updateRoom, name='update-room'),
    path("delete-room/<str:roomId>/", views.deleteRoom, name='delete-room'),
 
    path("delete-message/<str:messageId>/", views.deleteMessage, name='delete-message'),
]
