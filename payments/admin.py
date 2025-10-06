# In payments/admin.py

from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'provider', 'amount', 'status')
    list_filter = ('provider', 'status')
    search_fields = ('booking__id', 'provider_reference')