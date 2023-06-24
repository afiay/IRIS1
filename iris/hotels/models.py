from django.db import models
from django.conf import settings
from authenticate.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    cover_picture = models.ImageField(upload_to='media/hotel/hotel_covers/')
    hotel_logo = models.ImageField(upload_to='media/hotel/hotel_logos/')
    picture1 = models.ImageField(upload_to='media/hotel/hotel_pictures/', blank=True)
    picture2 = models.ImageField(upload_to='media/hotel/hotel_pictures/', blank=True)
    picture3 = models.ImageField(upload_to='media/hotel/hotel_pictures/', blank=True)
    picture4 = models.ImageField(upload_to='media/hotel/hotel_pictures/', blank=True)
    picture5 = models.ImageField(upload_to='media/hotel/hotel_pictures/', blank=True)
    picture6 = models.ImageField(upload_to='media/hotel/hotel_pictures/', blank=True)
    picture7 = models.ImageField(upload_to='media/hotel/hotel_pictures/', blank=True)
    picture8 = models.ImageField(upload_to='media/hotel/hotel_pictures/', blank=True)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_conference_facilities = models.BooleanField(default=False)
    has_room_service = models.BooleanField(default=False)
    has_bar = models.BooleanField(default=False)
    has_fitness_center = models.BooleanField(default=False)
    has_business_center = models.BooleanField(default=False)
    has_laundry_service = models.BooleanField(default=False)
    has_childcare = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)
    has_hot_tub = models.BooleanField(default=False)
    has_sauna = models.BooleanField(default=False)
    has_24_hour_front_desk = models.BooleanField(default=False)
    has_airport_shuttle = models.BooleanField(default=False)
    has_car_rental = models.BooleanField(default=False)
    has_currency_exchange = models.BooleanField(default=False)
    # Other hotel-related fields

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    picture1 = models.ImageField(upload_to='media/room/room_pictures/', blank=True)
    picture2 = models.ImageField(upload_to='media/room/room_pictures/', blank=True)
    picture3 = models.ImageField(upload_to='media/room/room_pictures/', blank=True)
    picture4 = models.ImageField(upload_to='media/room/room_pictures/', blank=True)
    picture5 = models.ImageField(upload_to='media/room/room_pictures/', blank=True)
    picture6 = models.ImageField(upload_to='media/room/room_pictures/', blank=True)
    picture7 = models.ImageField(upload_to='media/room/room_pictures/', blank=True)
    picture8 = models.ImageField(upload_to='media/room/room_pictures/', blank=True)
    # Other room-related fields

    def __str__(self):
        return f"Room {self.number} - {self.hotel.name}"

from django.db import models

class RoomAvailability(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='availabilities')
    date_from = models.DateField()
    date_to = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room} - From: {self.date_from} To: {self.date_to} (Available: {self.is_available})"




class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotel_bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField()
    # Other booking-related fields

    def __str__(self):
        return f"Booking ID: {self.id} - Room: {self.room.number} - {self.user.username}"
