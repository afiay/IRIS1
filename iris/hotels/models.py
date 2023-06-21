from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
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


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField()
    # Other booking-related fields

    def __str__(self):
        return f"Booking ID: {self.id} - Room: {self.room.number} - {self.user.username}"