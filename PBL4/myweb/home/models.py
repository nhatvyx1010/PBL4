from django.db import models
from django.forms import ModelForm, Textarea

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    avatar = models.ImageField(upload_to='/uploads/%Y/%m')
# Create your models here.
class User_Plate_Number(models.Model):
    user_id = models.CharField(primary_key=True, max_length=10)
    plate_number = models.CharField(max_length=20)
class user(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    def __str__(self):
        return self.user_id
class staff(models.Model):
    staff_id = models.CharField(primary_key=True, max_length=10)
    fullname = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    state = models.IntegerField(max_length=4)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    photo = models.CharField(max_length=255)
class Parking(models.Model):
    stt = models.IntegerField(primary_key=True, max_length=3)
    plate_number = models.ForeignKey(max_length=20)
    time_in = models.DateTimeField(auto_now_add=True)
class Parking_History(models.Model):
    plate_number = models.OneToOneField(Parking, max_length=20, on_delete=models.CASCADE, primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, max_length= 10)
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(max_length=3)
    total = models.FloatField()

class Login(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    state = models.IntegerField()
class Login_Staff(models.Model):
    id = models.OneToOneField(Login, primary_key=True, max_length=10, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE, max_length=10)
class Login_User(models.Model):
    id = models.OneToOneField(Login, primary_key=True, max_length=10, on_delete=models.CASCADE)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, max_length=10)
