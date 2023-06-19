from django import forms
from .models import Service, Rating, Booking

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'country', 'address', 'latitude', 'longitude', 'pictures', 'cover_picture',
                  'available_from', 'available_to', 'guest_limit']
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
        fields = ['service', 'user', 'from_date', 'to_date']
        widgets = {
            'service': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date > to_date:
            raise forms.ValidationError("The 'from' date must be before the 'to' date.")

        return cleaned_data
