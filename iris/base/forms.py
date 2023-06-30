from django import forms
from .models import Service, Rating, Booking

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'country', 'address', 'latitude', 'longitude', 'pictures', 'cover_picture',
                  'available_from', 'available_to', 'guest_limit', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'pictures': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'cover_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'available_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'available_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'guest_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'from_date', 'to_date', 'participants']
        widgets = {
            'service': forms.HiddenInput(),
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'participants': forms.NumberInput(attrs={'class': 'form-control'}),
        }

