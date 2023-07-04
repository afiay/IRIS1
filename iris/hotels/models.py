from datetime import timedelta
from django.db import models
from django.conf import settings
from authenticate.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q


class Hotel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    country = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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

    def __str__(self):
        return f"Room {self.number} - {self.hotel.name}"

    def is_date_range_available(self, start_date, end_date):
        return not self.bookings.filter(
            Q(check_in_date__lte=end_date, check_out_date__gte=start_date)
            | Q(check_in_date__gte=start_date, check_in_date__lte=end_date)
            | Q(check_out_date__gte=start_date, check_out_date__lte=end_date)
        ).exists()


class RoomAvailability(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField()
    end_date = models.DateField()
    is_available = models.BooleanField(default=True)
    is_unavailable = models.BooleanField(default=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.room} - From: {self.start_date} To: {self.end_date} (Price per night: {self.price_per_night})"

    def get_available_dates(self):
        return [self.start_date + timedelta(days=i) for i in range((self.end_date - self.start_date).days + 1)]

    def is_date_range_available(self, start_date, end_date):
        return self.is_available and not self.room.bookings.filter(
            Q(check_in_date__range=[start_date, end_date]) | Q(check_out_date__range=[start_date, end_date]) |
            (Q(check_in_date__lte=start_date) & Q(check_out_date__gte=end_date))
        ).exists()

    def delete(self, *args, **kwargs):
        bookings_to_cancel = self.room.bookings.filter(
            check_in_date__lte=self.end_date,
            check_out_date__gte=self.start_date
        )
        for booking in bookings_to_cancel:
            booking.delete()

        super().delete(*args, **kwargs)


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotel_bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Booking ID: {self.id} - Room: {self.room.number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.room.is_date_range_available(self.check_in_date, self.check_out_date):
            raise ValidationError('Room is not available for the selected dates.')

        num_nights = (self.check_out_date - self.check_in_date).days
        self.total_amount = num_nights * self.room.price_per_night

        super().save(*args, **kwargs)

        booked_dates = [self.check_in_date + timedelta(days=i) for i in range(num_nights)]
        availabilities_to_update = self.room.availabilities.filter(
            start_date__lte=self.check_out_date,
            end_date__gte=self.check_in_date
        )
        for availability in availabilities_to_update:
            availability.is_available = availability.end_date not in booked_dates
            availability.save()


class HotelRating(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    service = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.service}: {self.rating}"
