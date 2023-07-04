from django import forms
from .models import Booking, HotelRating, Room, RoomAvailability, Hotel

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests']

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            if check_in_date > check_out_date:
                raise forms.ValidationError("Check-in date cannot be after check-out date.")
            elif check_in_date == check_out_date:
                raise forms.ValidationError("Check-in date cannot be the same as check-out date.")

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'description', 'has_pool', 'has_gym', 'has_spa', 'has_restaurant', 'has_wifi',
                  'has_parking', 'has_conference_facilities', 'has_room_service', 'has_bar', 'has_fitness_center',
                  'has_business_center', 'has_laundry_service', 'has_childcare', 'has_swimming_pool', 'has_hot_tub',
                  'has_sauna', 'has_24_hour_front_desk', 'has_airport_shuttle', 'has_car_rental',
                  'has_currency_exchange']
        widgets = {
            'has_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_gym': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_spa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_restaurant': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_wifi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_conference_facilities': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_room_service': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_bar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_fitness_center': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_business_center': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_laundry_service': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_childcare': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_swimming_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_hot_tub': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_sauna': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_24_hour_front_desk': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_airport_shuttle': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_car_rental': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_currency_exchange': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'capacity', 'price_per_night', 'picture1', 'picture2', 'picture3', 'picture4', 'picture5',
                  'picture6', 'picture7', 'picture8']


class RoomAvailabilityForm(forms.ModelForm):
    class Meta:
        model = RoomAvailability
        fields = ['start_date', 'end_date', 'is_available', 'is_unavailable', 'price_per_night']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = HotelRating
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Rating',
            'comment': 'Comment',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
