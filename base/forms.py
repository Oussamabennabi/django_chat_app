from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
  class Meta:
    model = Room
    fields = "__all__"
    exclude = ['host', 'participants']

class UserCreate(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'avatar',
              'bio', 'fullname', 'password1', 'password2']



class UserUpdateForm(ModelForm):

  class Meta:
    model = User
    fields = ['username','email','avatar','bio','fullname']