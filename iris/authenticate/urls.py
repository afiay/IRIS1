from django.urls import path
from authentication.views import register, user_login

urlpatterns = [
    # Other URL patterns
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
]