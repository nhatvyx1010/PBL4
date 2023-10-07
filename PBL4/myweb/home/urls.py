from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('history/', views.history_admin, name="history"),
    path('index_staff/', views.index_staff, name="index_staff"),
    path('indexacc/', views.indexacc, name="indexacc"),
    path('history_acc/', views.history_acc, name="history_acc"),
    path('manager/', views.manager, name="manager"),
    path('index/', views.index, name="index"),
    

]
