from django import forms
from .models import Service, Rating, Booking

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'country', 'address', 'latitude', 'longitude', 'pictures', 'cover_picture',
                  'available_from', 'available_to', 'guest_limit']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']

from django import forms
from .models import Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'user', 'from_date', 'to_date']

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date > to_date:
            raise forms.ValidationError("The 'from' date must be before the 'to' date.")


        return cleaned_data
