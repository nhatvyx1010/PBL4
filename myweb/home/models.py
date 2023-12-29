from django.db import models
from django.utils import timezone
import random, string

def generate_random_user_id():
    random_number = random.randint(0, 999999)
    return f"user{random_number:08d}"  # Định dạng thành số có 4 chữ số


def generate_random_staff_id():
    random_number = random.randint(0, 999999)
    return f"user{random_number:08d}"  # Định dạng thành số có 4 chữ số

def generate_random_parking_history_id():
    random_number = random.randint(0, 999999)
    return f"park{random_number:08d}"  # Định dạng thành số có 4 chữ số

class LicensePlates(models.Model):
    license_platesID = models.CharField(max_length=15, primary_key=True)
    license_plates = models.CharField(max_length=15)

class LicensePlatesUser(models.Model):
    userID = models.CharField(max_length=15)
    license_plates = models.ForeignKey(LicensePlates, on_delete=models.CASCADE)

class LicensePlatesParking(models.Model):
    parking_historyID = models.CharField(max_length=15)
    license_plates = models.ForeignKey(LicensePlates, on_delete=models.CASCADE)

class ParkingHistory(models.Model):
    parking_historyID = models.CharField(max_length=15, primary_key=True, default=generate_random_parking_history_id())
    license_plates = models.ForeignKey(LicensePlates, on_delete=models.CASCADE, default='')
    state = models.IntegerField()
    date_in = models.DateField(default=timezone.now)
    date_out = models.DateField(null=True, blank=True)
    time_in = models.TimeField(default=timezone.now)
    time_out = models.TimeField(null=True)
    total = models.FloatField(default='0')
    note = models.TextField(default='')

class StaffParking(models.Model):
    staffID = models.CharField(max_length=15)
    parking_history = models.ForeignKey(ParkingHistory, on_delete=models.CASCADE)

class Staff(models.Model):
    staff_id = models.CharField(max_length=15, primary_key=True, default=generate_random_staff_id())
    fullname = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    position = models.CharField(max_length=255)
    state = models.IntegerField()
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    photo = models.CharField(max_length=255, null=True)

class User(models.Model):
    id = models.CharField(max_length=15, primary_key=True, default=generate_random_user_id())
    username = models.CharField(max_length=20,null=True)
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=255, null=True)
    fullname = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)
    position = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    account_balance = models.FloatField(default=0.0)
    role = models.CharField(max_length=10, null=True)
    photo = models.CharField(max_length=255, null=True)

