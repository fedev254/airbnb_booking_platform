from django.db import models
from django.conf import settings

def apartment_image_upload_path(instance, filename):
    return f'apartments/{instance.apartment.id}/{filename}'

class Apartment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='apartments')
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120, db_index=True)
    country = models.CharField(max_length=120, default='Kenya')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField(default=2)
    amenities = models.JSONField(default=list, blank=True)  # better than comma string
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['city','price_per_night']),
            models.Index(fields=['-created_at']),
        ]

class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=apartment_image_upload_path)
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']
