from rest_framework import serializers
from .models import Car, Rating


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id',
            'make',
            'model',
            'avg_rating',
        )


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'car_id',
            'rating',
        )


class CreateCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'make',
            'model',
        )


class CreateRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'car_id',
            'rating',
        )


class CarPopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id',
            'make',
            'model',
            'rates_number',
        )
