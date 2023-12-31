from django.urls import path
from .views import register, user_login, profile

urlpatterns = [
    # Other URL patterns
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('profile/', profile, name='profile'),
]
