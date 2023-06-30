from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, HotelRating, Room, Booking
from .forms import BookingForm, RatingForm, RoomForm, HotelForm
from django.db.models import Avg


from django.contrib.auth.decorators import login_required 

@login_required
def room_list(request, hotel_id=None):
    if hotel_id:
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        rooms = hotel.rooms.all()
    else:
        rooms = Room.objects.all()
    
    return render(request, 'room_list.html', {'rooms': rooms})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from .models import Room

@login_required
def booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            return redirect('booking_success', booking_id=booking.id)
    else:
        booking_form = BookingForm()

    return render(request, 'booking.html', {'room': room, 'booking_form': booking_form})

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})


from django.db.models import Q

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
            rooms__availabilities__date_from__lte=date_from,
            rooms__availabilities__date_to__gte=date_to,
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

    return render(request, 'hotel_list.html', context)


@login_required
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()

    return render(request, 'add_hotel.html', {'form': form})

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

    return render(request, 'edit_hotel.html', {'form': form, 'hotel': hotel})

@login_required
def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        hotel.delete()
        return redirect('hotel_list')

    return render(request, 'delete_hotel.html', {'hotel': hotel})
def get_rating_form(hotel, user):
    if not HotelRating.objects.filter(hotel=hotel, user=user).exists():
        return RatingForm()
    return None




from django.shortcuts import reverse

from .forms import RatingForm

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
            return redirect('hotel_detail', hotel_id=hotel_id)
    else:
        rating_form = RatingForm()

    return redirect('hotel_details', hotel_id=hotel_id)



def check_booking_availability(hotel, booking_form):
    if not hotel.availability:
        return False

    if booking_form.is_bound and booking_form.is_valid():
        from_date = booking_form.cleaned_data['from_date']
        to_date = booking_form.cleaned_data['to_date']
        
        if not hotel.is_date_range_available(from_date, to_date):
            booking_form.add_error('from_date', 'The selected dates are not available for booking.')
        else:
            return True

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

    return render(request, 'hotel_details.html', {
        'hotel': hotel,
        'ratings': ratings,
        'rating_form': rating_form,
        'booking_form': booking_form,
        'average_rating': average_rating,
    })




@login_required
def room_details(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            # Create a new booking instance
            booking = Booking(user=request.user, room=room, check_in=check_in, check_out=check_out)
            booking.save()
            return redirect('booking_confirmation')  # Redirect to a booking confirmation page

    context = {
        'room': room,
        'form': form,
    }

    return render(request, 'room_details.html', context)

@login_required
def room_list(request, hotel_id=None):
    if hotel_id:
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        rooms = hotel.rooms.all()
    else:
        rooms = Room.objects.all()
    
    return render(request, 'room_list.html', {'rooms': rooms})

@login_required
def room_add(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel  # Associate the room with the specified hotel
            room.save()
            return redirect('room_list', hotel_id=hotel_id)
    else:
        form = RoomForm()

    return render(request, 'room_add.html', {'form': form, 'hotel': hotel})

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

    return render(request, 'room_edit.html', {'form': form, 'room': room, 'hotel': hotel})

@login_required
def room_availability(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    availabilities = room.availabilities.all()

    # Filter availabilities based on date range if provided in the request
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from and date_to:
        availabilities = availabilities.filter(date__range=[date_from, date_to])

    context = {
        'room': room,
        'availabilities': availabilities,
        'date_from': date_from,
        'date_to': date_to
    }
    return render(request, 'availability.html', context)