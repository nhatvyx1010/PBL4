from django import forms
from .models import LicensePlates, LicensePlatesUser, LicensePlatesParking, ParkingHistory, StaffParking, Staff, User
class LicensePlates_Form(forms.ModelForm):
    class Meta:
        model = LicensePlates
        fields = "__all__"

class LicensePlatesUser_Form(forms.ModelForm):
    class Meta:
        model = LicensePlatesUser
        fields = "__all__"

class LicensePlatesParking_Form(forms.ModelForm):
    class Meta:
        model = LicensePlatesParking
        fields = "__all__"

class ParkingHistory_Form(forms.ModelForm):
    class Meta:
        model = ParkingHistory
        fields = "__all__"
class StaffParking_Form(forms.ModelForm):
    class Meta:
        model = StaffParking
        fields = "__all__"

class Staff_Form(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"

class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
