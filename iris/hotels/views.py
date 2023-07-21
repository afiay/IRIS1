from datetime import datetime, timedelta, date
import calendar
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q, Min, Max
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Hotel, HotelRating, Room, Booking, RoomAvailability
from .forms import BookingForm, RatingForm, RoomForm, HotelForm, RoomAvailabilityForm


@login_required
def room_list(request, hotel_id=None):
    """
    View for listing rooms in a hotel or all rooms if no hotel ID is provided.
    """
    if hotel_id:
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        rooms = hotel.rooms.all()
    else:
        rooms = Room.objects.all()
    return render(request, 'room/room_list.html', {'rooms': rooms})

import folium
from folium.plugins import MarkerCluster
from django.db.models import Q
from django.utils.html import escape
import json

@login_required
def hotel_list(request):
    """
    View for listing hotels based on various filters.
    """
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    guest_count = request.GET.get('guest_count')
    rate_filter = request.GET.get('rate')
    price_filter = request.GET.get('price')
    country_filter = request.GET.get('country')
    availability_filter = request.GET.get('availability')

    hotels = Hotel.objects.all().distinct()

    boolean_fields = [
        'has_pool',
        'has_gym',
        'has_spa',
        'has_restaurant',
        'has_wifi',
        'has_parking',
        'has_conference_facilities',
        'has_room_service',
        'has_bar',
        'has_fitness_center',
        'has_business_center',
        'has_laundry_service',
        'has_childcare',
        'has_swimming_pool',
        'has_hot_tub',
        'has_sauna',
        'has_24_hour_front_desk',
        'has_airport_shuttle',
        'has_car_rental',
        'has_currency_exchange',
    ]

    hotels = Hotel.objects.all().distinct()

    if date_from and date_to and guest_count:
        guest_count = int(guest_count)

        hotels = hotels.filter(
            rooms__capacity__gte=guest_count,
            rooms__availabilities__start_date__lte=date_from,
            rooms__availabilities__end_date__gte=date_to,
            rooms__availabilities__is_available=True
        ).distinct()

    if rate_filter:
        rate_filter = int(rate_filter)
        hotels = hotels.filter(ratings__rating=rate_filter)

    if price_filter:
        hotels = hotels.filter(rooms__price_per_night__gt=Decimal('0.00'))

    if country_filter:
        hotels = hotels.filter(country=country_filter)

    if availability_filter:
        hotels = hotels.filter(
            rooms__availabilities__start_date__lte=availability_filter,
            rooms__availabilities__end_date__gte=availability_filter,
            rooms__availabilities__is_available=True
        ).distinct()

    # Filter hotels based on selected amenities
    selected_amenities = [field.lower() for field in boolean_fields if request.GET.get(field)]
    if selected_amenities:
        filters = Q()
        for amenity in selected_amenities:
            filters |= Q(**{amenity: True})
        hotels = hotels.filter(filters)

    rates = [
        (1, range(1)),
        (2, range(2)),
        (3, range(3)),
        (4, range(4)),
        (5, range(5)),
    ]

    price_range = (
        hotels.aggregate(min_price=Min('rooms__price_per_night'))['min_price'] or 0,
        hotels.aggregate(max_price=Max('rooms__price_per_night'))['max_price'] or 0
    )
    # Create a list to hold hotel data for the map

    hotels_data = []
    for hotel in hotels:
        latitude = hotel.latitude
        longitude = hotel.longitude
        popup_html = (
            f'<img src="{escape(hotel.cover_picture.url)}" alt="Hotel Picture" style="width: 100px; height: auto;"><br>'
            f'<strong>{escape(hotel.name)}</strong><br>'
            f'{escape(hotel.address)}<br>'
            # Modified popup_html to include a link that opens the hotel details in a new tab
            f'<a href="{escape(reverse("hotel_details", args=[hotel.id]))}" target="_blank" class="btn btn-primary">View Details</a>'
        )
        hotels_data.append({
            'latitude': latitude,
            'longitude': longitude,
            'popup_html': popup_html,
            'name': hotel.name,
        })
    # Paginate the hotels queryset
    paginator = Paginator(hotels, 5)  # Set the desired number of hotels per page
    page_number = request.GET.get('page')
    hotels = paginator.get_page(page_number)
    # Generate the HTML representation of the hotel map
    hotel_map = folium.Map(location=[0, 0], zoom_start=2, attribution=None)
    # Remove the attribution (credit) from the map
    folium.TileLayer('openstreetmap', attr='').add_to(hotel_map)
    marker_cluster = MarkerCluster().add_to(hotel_map)

    for hotel_data in hotels_data:
        latitude = hotel_data['latitude']
        longitude = hotel_data['longitude']
        popup_html = hotel_data['popup_html']
        hotel_name = hotel_data['name']
        folium.Marker([latitude, longitude], popup=popup_html, tooltip=hotel_name).add_to(marker_cluster)

    # Generate the HTML representation of the hotel map
    hotel_map_html = hotel_map._repr_html_()

    context = {
        'hotels': hotels,
        'date_from': date_from,
        'date_to': date_to,
        'guest_count': guest_count,
        'rate_filter': rate_filter,
        'price_filter': price_filter,
        'country_filter': country_filter,
        'availability_filter': availability_filter,
        'rates': rates,
        'price_range': price_range,
        'boolean_fields': boolean_fields,
        'field_values': request.GET,
        'hotel_map': hotel_map_html,  # Add the hotel map to the template context
        'hotels_data': json.dumps(hotels_data),  # Add the hotels_data to the template context
    }

    return render(request, 'hotel/hotel_list.html', context)



@login_required
def add_hotel(request):
    """
    View for adding a new hotel.
    """
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
    """
    View for editing an existing hotel.
    """
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
    """
    View for deleting a hotel.
    """
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        hotel.delete()
        return redirect('hotel_list')
    return render(request, 'hotel/delete_hotel.html', {'hotel': hotel})


@login_required
def add_rating_hotel(request, hotel_id):
    """
    View for adding a rating to a hotel.
    """
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
    """
    View for displaying room details and availability.
    """
    room = get_object_or_404(Room, id=room_id)
    availabilities = room.availabilities.all()
    # Get the current month and year
    current_date = datetime.now()
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
    availability_dates = []
    availability_calendar = []
    for week in calendar.monthcalendar(year, month):
        week_data = []
        for day in week:
            if day != 0:
                date_obj = date(year, month, day)
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
        if check_booking_availability(room.hotel, booking_form):
            booking = booking_form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            room.hotel.availability = False
            room.hotel.save()
            return redirect('hotel_details', hotel_id=room.hotel.id)
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
    """
    View for displaying room availability.
    """
    room = get_object_or_404(Room, pk=room_id)
    availability_dates = room.availabilities.filter(start_date__gte=date.today()).values_list('start_date', flat=True)
    return render(request, 'room/room_availability.html', {'room': room, 'availability_dates': availability_dates})


@login_required
def room_add_availability(request, room_id):
    """
    View for adding room availability.
    """
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
    """
    View for adding a new room to a hotel.
    """
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
    """
    View for editing an existing room.
    """
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
    """
    View for deleting room availability.
    """
    room = get_object_or_404(Room, id=room_id)
    availability = get_object_or_404(RoomAvailability, id=availability_id, room=room)
    if request.method == 'POST':
        availability.delete()
        return redirect('room_details', room_id=room_id)
    return render(request, 'room/delete_availability.html', {'room': room, 'availability': availability})


@login_required
def edit_availability(request, room_id, availability_id):
    """
    View for editing room availability.
    """
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
    """
    View for deleting room availability.
    """
    room = get_object_or_404(Room, id=room_id)
    availability = get_object_or_404(RoomAvailability, id=availability_id, room=room)
    if request.method == 'POST':
        availability.delete()
        return redirect('room_details', room_id=room_id)
    return render(request, 'room/availability_delete.html', {'room': room, 'availability': availability})


@login_required
def edit_room(request, room_id):
    """
    View for editing an existing room.
    """
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
    """
    View for displaying hotel details and ratings.
    """
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


@login_required
def booking(request, room_id):
    """
    View for making a booking for a room.
    """
    room = get_object_or_404(Room, pk=room_id)
    availability = room.availabilities.first()
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if check_booking_availability(room.hotel, booking_form):
            booking = booking_form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            room.hotel.availability = False
            room.hotel.save()
            return redirect('hotel_details', hotel_id=room.hotel.id)
    else:
        booking_form = BookingForm()
    return render(request, 'hotel/booking.html', {'room': room, 'booking_form': booking_form, 'availability': availability})


@login_required
def booking_success(request, booking_id):
    """
    View for displaying a booking success message.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'room/booking_success.html', {'booking': booking})


def get_rating_form(hotel, user):
    """
    Helper function to get the rating form for a hotel and user.
    """
    if not HotelRating.objects.filter(hotel=hotel, user=user).exists():
        return RatingForm()
    return None


def check_booking_availability(hotel, booking_form):
    """
    Helper function to check the availability for a booking form.
    """
    check_in_date = booking_form.cleaned_data['check_in_date']
    check_out_date = booking_form.cleaned_data['check_out_date']
    guests = booking_form.cleaned_data['guests']

    if not hotel.availability:
        booking_form.add_error(None, 'No availability for the selected room.')
        return False

    availability = hotel.rooms.filter(availabilities__start_date__lte=check_in_date,
                                      availabilities__end_date__gte=check_out_date,
                                      availabilities__is_available=True).first()
    if not availability:
        booking_form.add_error(None, 'Selected dates are not available.')
        return False

    if guests > availability.room.capacity:
        booking_form.add_error('guests', 'The room capacity is exceeded.')
        return False

    return True
