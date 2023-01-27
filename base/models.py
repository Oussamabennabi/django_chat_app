from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# idididididi
class User(AbstractUser):
    username = models.CharField(max_length=200, null=True)
    fullname = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True,blank=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    pass


class Topic(models.Model):
  name = models.CharField(max_length=100)
  def __str__(self):
      return self.name


class Room(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    # only have one host and a topic
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # we add related_name atribute because we can not refrence the User twice thats why we need to change the name for participants for avoiding conflicts 
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)

    
    def __str__(self):
        return self.name

    class Meta:
      ordering = ['-updated_at','-created_at']

class Message(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  body = models.TextField() 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.body[0:50]
