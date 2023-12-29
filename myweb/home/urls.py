from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),

    path('historyStaff1/', views.historyStaff1, name="historyStaff1"),
    path('historyStaff/', views.history_staff, name="historyStaff"),
    path('indexStaff/', views.index_staff, name="indexStaff"),
    path('updateStaff/', views.update_staff, name='updateStaff'),
    path('managerStaff/User', views.managerStaff_User, name="managerStaff_User"),
    path('managerStaff/', views.manager_staff, name="managerStaff"),
    path('managerStaff_register', views.managerStaff_register, name="managerStaff_register"),
    path('managerStaff_delete', views.managerStaff_delete, name="managerStaff_delete"),
    path('historyStaff_delete', views.historyStaff_delete, name="historyStaff_delete"),
    

    path('indexUser/', views.index_user, name="indexUser"),
    path('updateUser/', views.update_user, name='updateUser'),
    path('historyUser/', views.history_user, name="historyUser"),
    path('addLicensePlate_User/', views.addLicensePlate_User, name='addLicensePlate_User'),

    path('index/', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('register', views.register_user, name="register"),

    path('contact/', views.contact.as_view(), name="contact"),
    path('contactDetail/', views.contactDetail, name="contactDetail"),
    path('contactView/', views.contactView, name="contactView"),

    path('camera_in/', views.video_feed_in, name='video_feed_in'),
    path('camera_out/', views.video_feed_out, name='video_feed_out'),
    # path('display_image/', views.display_image, name='display_image'),
    path('capture_image_in/', views.capture_image_in, name='capture_image_in'),
    path('capture_image_data/', views.capture_image_data, name='capture_image_data'),
    
    path('capture_image_out/', views.capture_image_out, name='capture_image_out'),
    # path('call_functions_once/', views.call_functions_once, name='call_functions_once'),

    path('historyIn/', views.historyIn, name='historyIn'),
    path('historyOut/', views.historyOut, name='historyOut'),

    path('getTotal/', views.getTotal, name='getTotal'),
    path('checkTotal/', views.checkTotal, name='checkTotal'),
    # ///////////////////
    path('api/module1/', views.module1_api, name='module1_api'),
]
