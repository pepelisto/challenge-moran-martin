from rest_framework import serializers
from .models import Listing, Special_price

class ListingSerializer(serializers.ModelSerializer):
    special_prices = serializers.StringRelatedField(many=True)
    class Meta:
        model = Listing
        fields = '__all__'

class Price_dateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Special_price
        fields = '__all__'

