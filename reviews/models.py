from django.db import models
from django.conf import settings
from apartments.models import Property, Unit


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews") 
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}/5 by {self.user} for {self.unit}"
