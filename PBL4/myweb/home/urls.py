from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),

    path('historyStaff1/', views.historyStaff1, name="historyStaff1"),
    path('historyStaff/', views.history_staff, name="historyStaff"),
    path('indexStaff/', views.index_staff, name="indexStaff"),
    path('updateStaff/', views.update_staff, name='updateStaff'),
    path('managerStaff1/', views.managerStaff1, name="managerStaff1"),
    path('managerStaff/', views.manager_staff, name="managerStaff"),
    path('managerStaff_register', views.managerStaff_register, name="managerStaff_register"),
    path('managerStaff_delete', views.managerStaff_delete, name="managerStaff_delete"),
    path('historyStaff_delete', views.historyStaff_delete, name="historyStaff_delete"),
    

    path('indexUser/', views.index_user, name="indexUser"),
    path('updateUser/', views.update_user, name='updateUser'),
    path('historyUser/', views.history_user, name="historyUser"),

    path('index/', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('register', views.register_user, name="register"),

    path('contact/', views.contact.as_view(), name="contact"),
    path('contactDetail/', views.contactDetail, name="contactDetail"),
    path('contactView/', views.contactView, name="contactView"),

]
