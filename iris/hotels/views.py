from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Room, Booking
from .forms import BookingForm, RoomForm, HotelForm


def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    rooms = hotel.rooms.all()
    return render(request, 'room_list.html', {'hotel': hotel, 'rooms': rooms})


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


def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel_list.html', {'hotels': hotels})


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
    return render(request, 'room_details.html', {'room': room})


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
