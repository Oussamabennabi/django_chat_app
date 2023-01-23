from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='Home'),
    path("login/", views.loginUser, name='login'),
    path("logout/", views.logoutUser, name='logout'),
    path("register/", views.registerUser, name='register'),
    path("room/<str:id>", views.room, name='Room'),
    path("create-room/", views.createRoom, name='create-room'),
    path("update-room/<str:roomId>/", views.updateRoom, name='update-room'),
    path("delete-room/<str:roomId>/", views.deleteRoom, name='delete-room'),
]
