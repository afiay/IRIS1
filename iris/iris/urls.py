from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from authenticate.views import register, user_login, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('hotel/', include('hotels.urls')),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('blog/', include('blog.urls')),

]
