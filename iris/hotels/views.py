from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, HotelRating, Room, Booking, RoomAvailability
from .forms import BookingForm, RatingForm, RoomForm, HotelForm, RoomAvailabilityForm
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
import calendar
from django.utils.timezone import now

@login_required
def room_list(request, hotel_id=None):
    if hotel_id:
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        rooms = hotel.rooms.all()
    else:
        rooms = Room.objects.all()
    return render(request, 'room/room_list.html', {'rooms': rooms})
@login_required
def hotel_list(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    guest_count = request.GET.get('guest_count')
    # Check if the filter parameters are provided
    if date_from and date_to and guest_count:
        guest_count = int(guest_count)

        # Filter hotels based on available rooms and capacity
        hotels = Hotel.objects.filter(
            rooms__capacity__gte=guest_count,
            rooms__availabilities__start_date__lte=date_from,
            rooms__availabilities__end_date__gte=date_to,
            rooms__availabilities__is_available=True
        ).distinct()
    else:
        # If the filter parameters are not provided, return all hotels
        hotels = Hotel.objects.all()
    context = {
        'hotels': hotels,
        'date_from': date_from,
        'date_to': date_to,
        'guest_count': guest_count
    }
    return render(request, 'hotel/hotel_list.html', context)
@login_required
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'hotel/add_hotel.html', {'form': form})
@login_required
def edit_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'hotel/edit_hotel.html', {'form': form, 'hotel': hotel})
@login_required
def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        hotel.delete()
        return redirect('hotel_list')
    return render(request, 'hotel/delete_hotel.html', {'hotel': hotel})
@login_required
def add_rating_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    user = request.user
    # Check if the user has already rated the hotel
    if HotelRating.objects.filter(hotel=hotel, user=user).exists():
        return redirect('hotel_details', hotel_id=hotel_id)
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.hotel = hotel
            rating.user = user
            rating.save()
            return redirect('hotel_details', hotel_id=hotel_id)

    return redirect('hotel_details', hotel_id=hotel_id)
@login_required
def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    availabilities = room.availabilities.all()
    # Get the current month and year
    current_date = now()
    year = current_date.year
    month = current_date.month
    # Check if there are request parameters for month and year
    if 'month' in request.GET and 'year' in request.GET:
        try:
            month = int(request.GET.get('month'))
            year = int(request.GET.get('year'))
        except ValueError:
            pass
    # Calculate the start and end date of the selected month
    start_date = datetime(year, month, 1)
    end_date = start_date.replace(day=calendar.monthrange(year, month)[1])
    # Generate the availability calendar for the selected month
 # Generate the availability calendar for the selected month
    availability_dates = []
    availability_calendar = []
    for week in calendar.monthcalendar(year, month):
        week_data = []
        for day in week:
            if day != 0:
                date_obj = datetime(year, month, day).date()
                availability = availabilities.filter(start_date__lte=date_obj, end_date__gte=date_obj).first()
                if availability and availability.is_available:
                    availability_dates.append(date_obj)
                    week_data.append((day, 'available'))
                else:
                    week_data.append((day, 'unavailable'))
            else:
                week_data.append(None)
        availability_calendar.append(week_data)

    # Check if a booking was made for the room
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            check_in_date = booking_form.cleaned_data['check_in_date']
            check_out_date = booking_form.cleaned_data['check_out_date']
            guests = booking_form.cleaned_data['guests']
            if availability and availability.is_available:
                if check_in_date >= availability.start_date and check_out_date <= availability.end_date:
                    if guests <= room.capacity:
                        booking = booking_form.save(commit=False)
                        booking.room = room
                        booking.user = request.user
                        booking.save()

                        # Update availability dates after booking
                        num_nights = (check_out_date - check_in_date).days
                        booked_dates = [check_in_date + timedelta(days=i) for i in range(num_nights)]
                        availability_dates = availability.get_available_dates()
                        availability_dates = list(set(availability_dates) - set(booked_dates))
                        availability.start_date = check_in_date
                        availability.end_date = check_out_date
                        availability.save()

                        return redirect('booking_success', booking_id=booking.id)
                    else:
                        booking_form.add_error('guests', 'The room capacity is exceeded.')
                else:
                    booking_form.add_error(None, 'Selected dates are not available.')
            else:
                booking_form.add_error(None, 'No availability for the selected room.')
    else:
        booking_form = BookingForm()

    context = {
        'room': room,
        'availabilities': availabilities,
        'availability_dates': availability_dates,
        'availability_calendar': availability_calendar,
        'current_month': month,
        'current_year': year,
        'prev_month': start_date.replace(day=1) - timedelta(days=1),
        'next_month': end_date.replace(day=calendar.monthrange(year, month)[1]) + timedelta(days=1),
        'booking_form': booking_form,
    }

    return render(request, 'room/room_details.html', context)

@login_required
def room_availability(request, room_id):
    room = Room.objects.get(pk=room_id)
    # Get today's date
    today = date.today()
    # Get the availability objects for the given room that have a start_date on or after today
    availability_dates = room.availabilities.filter(start_date__gte=today).values_list('start_date', flat=True)
    return render(request, 'room/room_availability.html', {'room': room, 'availability_dates': availability_dates})

@login_required
def room_add_availability(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        availability_form = RoomAvailabilityForm(request.POST)
        if availability_form.is_valid():
            availability = availability_form.save(commit=False)
            availability.room = room
            availability.save()
            return redirect('room_details', room_id=room_id)
    else:
        availability_form = RoomAvailabilityForm()
    return render(request, 'room/room_add_availability.html', {'availability_form': availability_form, 'room': room})

@login_required
def room_add(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        room_form = RoomForm(request.POST, prefix='room')
        availability_form = RoomAvailabilityForm(request.POST, prefix='availability')
        if room_form.is_valid() and availability_form.is_valid():
            room = room_form.save(commit=False)
            room.hotel = hotel
            room.user = request.user
            room.save()
            availability = availability_form.save(commit=False)
            availability.room = room
            availability.save()
            return redirect('hotel_details', hotel_id=hotel_id)
    else:
        room_form = RoomForm(prefix='room')
        availability_form = RoomAvailabilityForm(prefix='availability')
    return render(request, 'room/room_add.html', {'room_form': room_form, 'availability_form': availability_form, 'hotel': hotel})

@login_required
def room_edit(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    hotel = room.hotel
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'room/room_edit.html', {'form': form, 'room': room, 'hotel': hotel})

@login_required
def delete_availability(request, room_id, availability_id):
    room = get_object_or_404(Room, id=room_id)
    availability = get_object_or_404(RoomAvailability, id=availability_id, room=room)
    if request.method == 'POST':
        availability.delete()
        return redirect('room_details', room_id=room_id)
    return render(request, 'room/delete_availability.html', {'room': room, 'availability': availability})

@login_required
def edit_availability(request, room_id, availability_id):
    room = get_object_or_404(Room, id=room_id)
    availability = get_object_or_404(RoomAvailability, id=availability_id)
    if request.method == 'POST':
        form = RoomAvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            return redirect('room_details', room_id=room.id)
        else:
            # Handle invalid form
            pass
    else:
        form = RoomAvailabilityForm(instance=availability)
    context = {
        'room': room,
        'availability': availability,
        'form': form
    }
    return render(request, 'room/edit_availability.html', context)

@login_required
def availability_delete(request, room_id, availability_id):
    room = get_object_or_404(Room, id=room_id)
    availability = get_object_or_404(RoomAvailability, id=availability_id, room=room)
    if request.method == 'POST':
        availability.delete()
        return redirect('room_details', room_id=room_id)
    return render(request, 'room/availability_delete.html', {'room': room, 'availability': availability})

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_details', room_id=room.id)
    else:
        form = RoomForm(instance=room)

    return render(request, 'room/edit_room.html', {'form': form, 'room': room})


@login_required
def hotel_details(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    ratings = hotel.ratings.all()
    booking_form = BookingForm()
    rating_form = get_rating_form(hotel, request.user)
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if check_booking_availability(hotel, booking_form):
            booking = booking_form.save(commit=False)
            booking.hotel = hotel
            booking.user = request.user
            booking.save()
            hotel.availability = False
            hotel.save()
            return redirect('hotel_details', hotel_id=hotel_id)

    # Calculate the average rating using Django's Avg function
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST' and 'cover_picture' in request.FILES:
        cover_picture = request.FILES['cover_picture']
        hotel.cover_picture = cover_picture
        hotel.save()
    return render(request, 'hotel/hotel_detail.html', {
        'hotel': hotel,
        'ratings': ratings,
        'rating_form': rating_form,
        'booking_form': booking_form,
        'average_rating': average_rating,
    })

def get_rating_form(hotel, user):
    if not HotelRating.objects.filter(hotel=hotel, user=user).exists():
        return RatingForm()
    return None

from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorList
from datetime import timedelta
from django.shortcuts import get_object_or_404

@login_required
def booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    availability = room.availabilities.first()  # Get the first availability associated with the room, adjust the logic as needed
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            check_in_date = booking_form.cleaned_data['check_in_date']
            check_out_date = booking_form.cleaned_data['check_out_date']
            guests = booking_form.cleaned_data['guests']

            if availability and availability.is_available:
                if check_in_date >= availability.start_date and check_out_date <= availability.end_date:
                    if guests <= room.capacity:
                        booking = booking_form.save(commit=False)
                        booking.room = room
                        booking.user = request.user
                        booking.save()

                        # Update availability dates after booking
                        num_nights = (check_out_date - check_in_date).days
                        booked_dates = [check_in_date + timedelta(days=i) for i in range(num_nights)]
                        availability_dates = availability.get_available_dates()
                        availability_dates = list(set(availability_dates) - set(booked_dates))
                        availability.start_date = check_in_date
                        availability.end_date = check_out_date
                        availability.save()
                        return redirect('booking_success', booking_id=booking.id)
                    else:
                        booking_form.add_error('guests', 'The room capacity is exceeded.')
                else:
                    booking_form.add_error(None, 'Selected dates are not available.')
            else:
                booking_form.add_error(None, 'No availability for the selected room.')
    else:
        booking_form = BookingForm()
    return render(request, 'hotel/booking.html', {'room': room, 'booking_form': booking_form, 'availability': availability})

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'room/booking_success.html', {'booking': booking})