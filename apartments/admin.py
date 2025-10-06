# In apartments/admin.py

from django.contrib import admin
from .models import Apartment, ApartmentImage

class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage
    extra = 1  # How many extra forms to show
    readonly_fields = ('id',)

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price_per_night', 'owner', 'is_active')
    list_filter = ('city', 'country', 'is_active')
    search_fields = ('title', 'description', 'city')
    inlines = [ApartmentImageInline]