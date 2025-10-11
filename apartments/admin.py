# In apartments/admin.py

from django.contrib import admin
from .models import Property, Unit, UnitImage, BlockedDate

# This allows us to add multiple units directly when editing a property page
class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1  # Show one extra blank form for a new unit
    show_change_link = True

# This allows us to add multiple images directly when editing a unit page
class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'owner', 'is_active')
    list_filter = ('city', 'country', 'is_active')
    search_fields = ('title', 'description', 'city')
    # When you view a Property in the admin, you can see and edit its Units directly
    inlines = [UnitInline]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'property', 'price_per_night', 'max_guests', 'is_active')
    list_filter = ('property__city', 'is_active')
    search_fields = ('unit_name_or_number', 'property__title')
    # When you view a Unit, you can add/edit its images directly
    inlines = [UnitImageInline]

@admin.register(BlockedDate)
class BlockedDateAdmin(admin.ModelAdmin):
    list_display = ('unit', 'start_date', 'end_date', 'reason')
    list_filter = ('unit__property__city',)