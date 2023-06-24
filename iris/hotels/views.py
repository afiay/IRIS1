from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Room, Booking
from .forms import BookingForm, RoomForm, HotelForm



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



def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})


from django.db.models import Q

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



def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()

    return render(request, 'add_hotel.html', {'form': form})


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


def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        hotel.delete()
        return redirect('hotel_list')

    return render(request, 'delete_hotel.html', {'hotel': hotel})


def hotel_details(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    amenities = [
        [
            {'icon': 'fas fa-swimming-pool', 'name': 'Pool'},
            {'icon': 'fas fa-dumbbell', 'name': 'Gym'},
            {'icon': 'fas fa-spa', 'name': 'Spa'},
            {'icon': 'fas fa-utensils', 'name': 'Restaurant'},
            {'icon': 'fas fa-wifi', 'name': 'Free Wi-Fi'},
            {'icon': 'fas fa-parking', 'name': 'Parking'},
            {'icon': 'fas fa-chalkboard-teacher', 'name': 'Conference Facilities'},
            {'icon': 'fas fa-concierge-bell', 'name': 'Room Service'},
            {'icon': 'fas fa-glass-martini', 'name': 'Bar'},
        ],
        [
            {'icon': 'fas fa-dumbbell', 'name': 'Fitness Center'},
            {'icon': 'fas fa-briefcase', 'name': 'Business Center'},
            {'icon': 'fas fa-tshirt', 'name': 'Laundry Service'},
            {'icon': 'fas fa-baby', 'name': 'Childcare'},
            {'icon': 'fas fa-swimming-pool', 'name': 'Swimming Pool'},
            {'icon': 'fas fa-hot-tub', 'name': 'Hot Tub'},
            {'icon': 'fas fa-spa', 'name': 'Sauna'},
            {'icon': 'fas fa-clock', 'name': '24-Hour Front Desk'},
            {'icon': 'fas fa-shuttle-van', 'name': 'Airport Shuttle'},
            {'icon': 'fas fa-car', 'name': 'Car Rental'},
            {'icon': 'fas fa-money-bill-wave', 'name': 'Currency Exchange'},
        ]
        # Add more amenity groups as needed
    ]
    return render(request, 'hotel_details.html', {'hotel': hotel, 'amenities': amenities})




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


def room_list(request, hotel_id=None):
    if hotel_id:
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        rooms = hotel.rooms.all()
    else:
        rooms = Room.objects.all()
    
    return render(request, 'room_list.html', {'rooms': rooms})

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