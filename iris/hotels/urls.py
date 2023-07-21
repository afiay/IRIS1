from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('room/list/', views.room_list, name='room_list'),
    path('room/list/<int:hotel_id>/', views.room_list, name='room_list_by_hotel'),
    path('room/booking/<int:room_id>/', views.booking, name='booking'),
    path('room/booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('hotel/list/', views.hotel_list, name='hotel_list'),
    path('hotel/add/', views.add_hotel, name='add_hotel'),
    path('hotel/edit/<int:hotel_id>/', views.edit_hotel, name='edit_hotel'),
    path('hotel/delete/<int:hotel_id>/', views.delete_hotel, name='delete_hotel'),
    path('hotel/rating/add/<int:hotel_id>/', views.add_rating_hotel, name='add_rating_hotel'),
    path('room/details/<int:room_id>/', views.room_details, name='room_details'),
    path('room/availability/<int:room_id>/', views.room_availability, name='room_availability'),
    path('room/add/<int:hotel_id>/', views.room_add, name='room_add'),
    path('room/edit/<int:room_id>/', views.room_edit, name='room_edit'),
    path('room/add_availability/<int:room_id>/', views.room_add_availability, name='room_add_availability'),
    path('hotel/room/availability/delete/<int:room_id>/<int:availability_id>/', views.delete_availability, name='delete_availability'),
    path('room/availability/edit/<int:room_id>/<int:availability_id>/', views.edit_availability, name='edit_availability'),
    path('room/availability/delete/<int:room_id>/<int:availability_id>/', views.availability_delete, name='availability_delete'),
    path('room/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('hotels/<int:hotel_id>/', views.hotel_details, name='hotel_details'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
