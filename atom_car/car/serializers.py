from rest_framework import serializers
from django.utils import timezone
from car.models import *


class TrunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trunk
        fields = '__all__'


class WiperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wiper
        fields = '__all__'


class GlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glass
        fields = '__all__'


class GlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glass
        fields = '__all__'


class ClimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climate
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'


class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = '__all__'