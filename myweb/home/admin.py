from django.contrib import admin

from .models import LicensePlatesUser, LicensePlates, LicensePlatesParking, ParkingHistory, StaffParking, Staff, User
# Register your models here.

admin.site.register(LicensePlatesUser)
admin.site.register(LicensePlates)
admin.site.register(LicensePlatesParking)
admin.site.register(ParkingHistory)
admin.site.register(StaffParking)
admin.site.register(Staff)
admin.site.register(User)
