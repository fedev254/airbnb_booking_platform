# In apartments/serializers.py

from rest_framework import serializers
from .models import Property, Unit, UnitImage, BlockedDate
from core.serializers import UserSerializer
from datetime import date

# --- Core Public-Facing Serializers ---

class UnitImageSerializer(serializers.ModelSerializer):
    """Serializer for viewing unit images."""
    class Meta:
        model = UnitImage
        fields = ['id', 'image', 'caption', 'order']

#class SimplePropertySerializer(serializers.ModelSerializer):
    #"""Contains only essential property info for nesting."""
    #class Meta:
        #model = Property
        #fields = ['id', 'title', 'address', 'city']

class UnitSerializer(serializers.ModelSerializer):
    """Serializer for viewing individual units."""
    images = UnitImageSerializer(many=True, read_only=True)
    #property = SimplePropertySerializer(read_only=True)
    class Meta:
        model = Unit
        fields = '__all__'
class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer for the Property model, used for LIST views.
    Shows owner details. The owner is set automatically in the view.
    """
    owner = UserSerializer(read_only=True)
    #units = UnitSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = [
            'id', 'owner', 'title', 'description', 'address', 'city',
            'country', 'is_active', 'created_at'
        ]


class PropertyDetailSerializer(PropertySerializer):
    """
    Serializer for a single property's DETAIL view. Includes nested units.
    """
    units = UnitSerializer(many=True, read_only=True)

    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields + ['units']
    def get_units(self, obj):
        """
        This method is called to get the value for the 'units' field.
        We filter for active units belonging to this specific property ('obj').
        """
        # Filter for units that are active AND belong to the current property instance.
        active_units = obj.units.filter(is_active=True)
        
        # Serialize the filtered queryset using the UnitSerializer.
        # We pass 'many=True' because it's a list of units.
        # We must also pass the context to any nested serializers if they need it.
        serializer = UnitSerializer(active_units, many=True, context=self.context)
        
        # Return the serialized data.
        return serializer.data


# --- Host Management Serializers ---

class BlockedDateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing BlockedDate entries for a host.
    """
    unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all() # We filter for ownership in the validation
    )

    class Meta:
        model = BlockedDate
        fields = ['id', 'unit', 'start_date', 'end_date', 'reason']

    def validate_unit(self, unit):
        """Ensures the unit belongs to the logged-in host."""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        
        if unit.property.owner != request.user:
            raise serializers.ValidationError("You do not have permission to manage this unit.")
        return unit

    def validate(self, data):
        """Validates dates and checks for overlapping blocks."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")

        # Check for overlapping blocks for the same unit
        queryset = BlockedDate.objects.filter(
            unit=data.get('unit'),
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        # If we are updating an existing instance, exclude it from the check
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError("This unit already has an overlapping blocked date range.")

        return data

class UnitImageUploadSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for handling the upload of an image file.
    The 'unit' is associated in the view, not provided by the user.
    """
    class Meta:
        model = UnitImage
        fields = ['id', 'image', 'caption']