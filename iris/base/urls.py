from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('service/<int:service_id>/add_rating/', views.add_rating, name='add_rating'),
    path('add_service/', views.add_service, name='add_service'),
    path('booking/<int:service_id>/', views.booking, name='booking'),
    path('booking/<int:booking_id>/success/', views.booking_success, name='booking_success'),
    # Other URL patterns
    path('service/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('service/delete/<int:service_id>/', views.confirm_delete_service, name='confirm_delete_service'),
    # Other URL patterns



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
