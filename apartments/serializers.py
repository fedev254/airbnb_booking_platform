# In apartments/serializers.py

from rest_framework import serializers
from .models import Apartment, ApartmentImage
from core.serializers import UserSerializer

class ApartmentImageSerializer(serializers.ModelSerializer):
    """Serializer for apartment images."""
    class Meta:
        model = ApartmentImage
        fields = ['id', 'image', 'caption', 'order']


class ApartmentSerializer(serializers.ModelSerializer):
    """Serializer for the Apartment model. Includes nested images and owner info."""
    images = ApartmentImageSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True) # Read-only owner details

    class Meta:
        model = Apartment
        fields = [
            'id', 'owner', 'title', 'description', 'address', 'city', 'country',
            'price_per_night', 'max_guests', 'amenities', 'is_active',
            'created_at', 'images'
        ]
        read_only_fields = ['owner', 'created_at']

    def create(self, validated_data):
        # Automatically assign the logged-in user as the owner
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)