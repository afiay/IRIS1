from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Sum


class Service(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pictures = models.ImageField(upload_to='media/')
    available_from = models.DateField()
    available_to = models.DateField()
    guest_limit = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True, null=True, blank=True)
    cover_picture = models.ImageField(upload_to='media/service_covers/')
    service_description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    def average_rating(self) -> float:
        return Rating.objects.filter(service=self).aggregate(Avg("rating"))["rating__avg"] or 0
    def clean(self):
        super().clean()

        if self.available_from and self.available_to and self.available_from > self.available_to:
            raise ValidationError("The 'Available From' date must be before the 'Available To' date.")
        
    def __str__(self):
        return f"{self.name}: {self.average_rating()}"



class Rating(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.service.name}: {self.rating}"

from django.core.exceptions import ValidationError
class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    participants = models.PositiveIntegerField()

    def clean(self):
        super().clean()

        if self.from_date is not None and self.to_date is not None:
            if self.from_date > self.to_date:
                raise ValidationError("From date cannot be after the to date.")

        overlapping_bookings = Booking.objects.filter(
            service=self.service,
            from_date__lte=self.to_date,
            to_date__gte=self.from_date
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError("The selected dates are not available for booking.")

        guest_count = Booking.objects.filter(service=self.service).aggregate(Sum('participants'))['participants__sum']
        if guest_count is not None and (guest_count + self.participants) > self.service.guest_limit:
            raise ValidationError("The total number of participants exceeds the guest limit for this activity.")
    @property
    def total_price(self):
        duration = (self.to_date - self.from_date).days + 1
        return duration * self.service.price
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.service.availability = True
        self.service.save()


