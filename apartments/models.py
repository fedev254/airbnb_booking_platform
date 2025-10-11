
from django.db import models
from django.conf import settings

class Property(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120, db_index=True)
    country = models.CharField(max_length=120, default='Kenya')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) # Overall status of the property

    class Meta:
        verbose_name_plural = "Properties" # Correct pluralization

    def __str__(self):
        return self.title

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    unit_name_or_number = models.CharField(max_length=100) # e.g., "Unit A-101", "Penthouse"
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField(default=2)
    amenities = models.JSONField(default=list, blank=True)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True) # Status of the individual unit

    class Meta:
        ordering = ['unit_name_or_number']

    def __str__(self):
        return f"{self.property.title} - {self.unit_name_or_number}"

# --- 3. Modified Image Model to point to 'Unit' ---
def unit_image_upload_path(instance, filename):
    return f'units/{instance.unit.id}/{filename}'

class UnitImage(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=unit_image_upload_path)
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

# In apartments/models.py
# ... (existing imports and models are unchanged) ...

# --- Add this new model at the end of the file ---
class BlockedDate(models.Model):
    """
    Represents a date range when a specific unit is not available for booking.
    """
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='blocked_dates')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., Maintenance, Owner stay")

    class Meta:
        ordering = ['start_date']
        # Add a constraint to ensure end_date is after start_date
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F('start_date')),
                name='end_date_after_start_date'
            )
        ]

    def __str__(self):
        return f"Blocked: {self.unit} from {self.start_date} to {self.end_date}"