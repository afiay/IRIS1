# IRIS Booking

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-3.2%2B-green)](https://www.djangoproject.com/download/)
<p align="center"><img src="./readme_assets/home.jpg"></p>
## Description

Your Application Name is a web application built with Django that allows users to find and book hotels based on various filters, check room availability, and leave ratings and reviews for the hotels they have visited.

## Features

- User Registration and Authentication: Users can sign up, log in, and log out to access the application's features.
- Hotel Listings: Users can view a list of hotels with details, including name, address, amenities, and ratings.
- Hotel Filtering: Users can filter hotels based on criteria such as date, guest count, price range, amenities, and location.
- Hotel Details: Users can view detailed information about a specific hotel, including rooms, availability, and ratings.
- Hotel Ratings: Users can leave ratings and reviews for hotels they have visited.
- Room Booking: Users can book rooms in hotels based on availability and guest count.
- Map View: Hotels are displayed on a map for easy visualization of their locations.
- Admin Panel: An admin panel is available for managing hotels, rooms, bookings, and user ratings.

## Technologies Used

- Python
- Django
- HTML, CSS, JavaScript
- Bootstrap
- Folium (for map integration)
- PostgreSQL (or any other database supported by Django)

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
