from django.db import models
from bookings.models import Booking
from django.contrib.postgres.fields import JSONField

class Payment(models.Model):
    PROVIDER_CHOICES = [('mpesa','Mpesa'),('stripe','Stripe')]
    STATUS_CHOICES = [('initiated','initiated'),('success','success'),('failed','failed')]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    provider_reference = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
