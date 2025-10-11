# In bookings/admin.py

from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # --- CHANGE: 'apartment' is now 'unit' ---
    list_display = ('id', 'unit', 'user', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status', 'check_in', 'check_out')
    # --- CHANGE: Search by the unit's parent property title ---
    search_fields = ('unit__property__title', 'user__email')