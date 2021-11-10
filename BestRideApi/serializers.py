from django.core.serializers import serialize
from rest_framework import serializers
from .models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class InterestPointsSerializaer(serializers.ModelSerializer):
    class Meta:
        model = PointInterest
        fields = ('__all__')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RoadMapSerializer(serializers.ModelSerializer):
    city_id = CitySerializer(read_only=True)
    class Meta:
        model = RoadMap
        geo_field = "point"
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class RoadVehicleSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(many=False)

    class Meta:
        model = RoadVehicle
        fields = '__all__'


class ItinearyRouteSerializer(serializers.ModelSerializer):
    interest_points = InterestPointsSerializaer(read_only=True)
    class Meta:
        model = ItinearyRoute
        fields = ('interest_points',)

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class TravelScheduleSerializer(serializers.ModelSerializer):
    road_map_id = RoadMapSerializer(read_only=True)
    class Meta:
        model = TravelSchedule
        fields = '__all__'

class TravelSerializer(serializers.ModelSerializer):
    road_map_id = RoadMapSerializer()
    class Meta:
        model = Travel
        fields = '__all__'
