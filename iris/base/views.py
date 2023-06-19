from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Service, Rating, Booking
from .forms import BookingForm, RatingForm
from django.utils import timezone
from .forms import ServiceForm
from datetime import datetime


@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()
            return redirect('home')
    else:
        form = ServiceForm()

    return render(request, 'add_service.html', {'form': form})

from datetime import datetime

def home(request):
    # Retrieve filter parameters from the request
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')
    participants = request.GET.get('participants')
    category = request.GET.get('category')
    country = request.GET.get('country')

    # Convert date strings to date objects
    from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date() if from_date_str else None
    to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date() if to_date_str else None

    # Apply filters to the service queryset
    services = Service.objects.all()
    if from_date:
        services = services.filter(available_from__gte=from_date)
    if to_date:
        services = services.filter(available_to__lte=to_date)
    if participants:
        services = services.filter(guest_limit__gte=participants)
    if category:
        services = services.filter(category=category)
    if country:
        services = services.filter(country=country)

    # Retrieve category and country options for the filter dropdowns
    categories = Service.objects.values_list('category', flat=True).distinct()
    countries = Service.objects.values_list('country', flat=True).distinct()
    selected_category = category
    selected_country = country

    context = {
        'services': services,
        'from_date': from_date_str,
        'to_date': to_date_str,
        'participants': participants,
        'categories': categories,
        'countries': countries,
        'selected_category': selected_category,
        'selected_country': selected_country,
    }
    return render(request, 'home.html', context)



def get_service(service_id):
    return get_object_or_404(Service, pk=service_id)


def get_rating_form(service, user):
    if not Rating.objects.filter(service=service, user=user).exists():
        return RatingForm()
    return None


def check_booking_availability(service, booking_form):
    if not service.availability:
        return False

    if booking_form.is_bound and booking_form.is_valid():
        from_date = booking_form.cleaned_data['from_date']
        to_date = booking_form.cleaned_data['to_date']
        
        if not service.is_date_range_available(from_date, to_date):
            booking_form.add_error('from_date', 'The selected dates are not available for booking.')
        else:
            return True

    return False
@login_required
def service_detail(request, service_id):
    service = get_service(service_id)
    ratings = service.ratings.all()
    booking_form = BookingForm()
    rating_form = get_rating_form(service, request.user)
    
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if check_booking_availability(service, booking_form):
            booking = booking_form.save(commit=False)
            booking.service = service
            booking.user = request.user
            booking.save()
            service.availability = False
            service.save()
            return redirect('service_detail', service_id=service_id)

    average_rating = service.average_rating()

    if request.method == 'POST' and 'cover_picture' in request.FILES:
        cover_picture = request.FILES['cover_picture']
        service.cover_picture = cover_picture
        service.save()

    return render(request, 'service_detail.html', {
        'service': service,
        'ratings': ratings,
        'rating_form': rating_form,
        'booking_form': booking_form,
        'average_rating': average_rating,
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Rating
from .forms import RatingForm

@login_required
def add_rating(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    user = request.user

    # Check if the user has already rated the service
    if Rating.objects.filter(service=service, user=user).exists():
        return redirect('service_detail', service_id=service_id)

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.service = service
            rating.user = user
            rating.save()
            return redirect('service_detail', service_id=service_id)
    else:
        rating_form = RatingForm()

    return render(request, 'add_rating.html', {'service': service, 'rating_form': rating_form})


def booking(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        booking_form = BookingForm(request.POST, initial={'service': service})
        if booking_form.is_valid():
            # Process the booking
            booking = booking_form.save(commit=False)
            booking.service = service
            booking.user = request.user
            booking.save()
            service.availability = False
            service.save()
            return redirect('booking_success', booking_id=booking.id)
    else:
        booking_form = BookingForm(initial={'service': service})

    if service.availability:
        return render(request, 'booking.html', {'booking_form': booking_form, 'service': service})
    else:
        return HttpResponse("Service is not currently available for booking.")


from django.shortcuts import render, get_object_or_404

from .models import Booking

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})
