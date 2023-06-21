from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/rooms/', views.room_list, name='room_list'),
    path('room/<int:room_id>/booking/', views.booking, name='booking'),
    path('booking/<int:booking_id>/success/', views.booking_success, name='booking_success'),
    path('hotel/add/', views.add_hotel, name='add_hotel'),
    path('hotel/edit/<int:hotel_id>/', views.edit_hotel, name='edit_hotel'),
    path('hotel/delete/<int:hotel_id>/', views.delete_hotel, name='delete_hotel'),
    path('hotel/<int:hotel_id>/', views.hotel_details, name='hotel_details'),
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('room/list/', views.room_list, name='room_list'),
    path('room/add/<int:hotel_id>/', views.room_add, name='room_add'),
    path('room/edit/<int:room_id>/', views.room_edit, name='room_edit'),

]
