# In apartments/filters.py

from django_filters import rest_framework as filters
from .models import Property, Unit, BlockedDate
from bookings.models import Booking
from django.db.models import Q
from datetime import datetime


class PropertyFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_keyword', label="Search by city, property title, or address")
    
    # You could add other property-level filters here later, e.g., filter by amenities_available
    
    class Meta:
        model = Property
        fields = ['search']

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(city__icontains=value) |
            Q(address__icontains=value)
        )
class UnitFilter(filters.FilterSet):
    """
    FilterSet for the Unit model to enable searching and filtering.
    """
    # Filter by properties of the parent Property
    city = filters.CharFilter(field_name='property__city', lookup_expr='icontains')
    search = filters.CharFilter(method='filter_by_keyword', label="Search by city, property title, or address")
    # Filter by properties of the Unit itself
    min_price = filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    min_guests = filters.NumberFilter(field_name='max_guests', lookup_expr='gte')
    bedrooms = filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    
    # Advanced availability filter
    check_in = filters.DateFilter(method='filter_by_availability')
    check_out = filters.DateFilter(method='filter_by_availability')
    
    class Meta:
        model = Unit
        fields = ['search', 'city', 'min_price', 'max_price', 'min_guests', 'bedrooms', 'check_in', 'check_out']


    def filter_by_keyword(self, queryset, name, value):
        """
        Search for a keyword in property title, city, and address.
        Uses Q objects for a complex OR query.
        """
        return queryset.filter(
            Q(property__title__icontains=value) |
            Q(property__city__icontains=value) |
            Q(property__address__icontains=value)
        )
    def filter_by_availability(self, queryset, name, value):
        check_in_str = self.data.get('check_in')
        check_out_str = self.data.get('check_out')

        if check_in_str and check_out_str:
            check_in_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()

            # --- LOGIC for finding unavailable units ---

            # 1. Find units with conflicting BOOKINGS (this is our existing logic)
            booked_unit_ids = Booking.objects.filter(
                status__in=[Booking.STATUS_CONFIRMED, Booking.STATUS_PENDING],
                check_in__lt=check_out_date,
                check_out__gt=check_in_date
            ).values_list('unit_id', flat=True)

            # 2. Find units with conflicting BLOCKED DATES (this is the new logic)
            blocked_unit_ids = BlockedDate.objects.filter(
                start_date__lt=check_out_date,
                end_date__gt=check_in_date
            ).values_list('unit_id', flat=True)

            # 3. Combine the two lists of unavailable unit IDs
            unavailable_unit_ids = set(booked_unit_ids) | set(blocked_unit_ids)

            # --- 4. Exclude all unavailable units from the final queryset ---
            return queryset.exclude(id__in=unavailable_unit_ids)
        
        return queryset