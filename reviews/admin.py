# In reviews/admin.py

from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # --- CHANGE: 'apartment' is now 'property' ---
    list_display = ('id', 'property', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    # --- CHANGE: Search by the property's title ---
    search_fields = ('property__title', 'user__email', 'comment')