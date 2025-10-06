from django.db import models
from django.conf import settings
from apartments.models import Apartment
from django.db.models import Q, CheckConstraint, F

class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [(STATUS_PENDING,'Pending'),(STATUS_CONFIRMED,'Confirmed'),(STATUS_CANCELLED,'Cancelled'),(STATUS_COMPLETED, 'Completed')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField(db_index=True)
    check_out = models.DateField(db_index=True)
    guests = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(check_out__gt=F('check_in')), name='check_out_after_check_in'),
        ]

    def __str__(self):
        return f"Booking {self.id} ({self.apartment})"
