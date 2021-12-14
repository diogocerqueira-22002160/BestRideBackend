import logging

from botocore.exceptions import ClientError
from django.http import JsonResponse
from rest_framework.reverse import reverse
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from BestRideApi.serializers import *
from rest_framework_gis.pagination import GeoJsonPagination
from django.contrib.gis.geos import Point
from environs import Env
import math
import urllib3

env = Env()
env.read_env()

import boto3


class Routes(APIView):

    @api_view(['POST'])
    def getRoadMap(request):
        KM_MAX = request.data['kmMAX']
        Road = RoadMap.objects.all()
        boto3.setup_default_session(region_name='us-east-2')
        s3_client = boto3.client('s3')

        distance_dict = {}

        for rd in Road:
            p1 = Point(request.data['lat'],request.data['lng'])
            p2 = Point(rd.location.coords[0],rd.location.coords[1])
            distance = p1.distance(p2)
            distance_in_km = math.trunc(distance * 100)
            distance_dict[str(rd.title)] = distance_in_km

        for name,km in distance_dict.items():
            if km > KM_MAX:
                Road = Road.exclude(title=name)

        try:
            for e in Road:
                response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'bestridebucket',
                                                                'Key': '' + e.image},
                                                        ExpiresIn=3600)
                e.image = response

        except ClientError as e:
            logging.error(e)

        Road_Serializer = RoadMapSerializer(Road,many=True)
        return Response(Road_Serializer.data)

    @api_view(['POST'])
    def distance(request):
        Road = RoadMap.objects.all()

        distance_dict = {}

        for rd in Road:
            p1 = Point(request.data['lat'],request.data['lng'])
            p2 = Point(rd.location.coords[0],rd.location.coords[1])
            distance = p1.distance(p2)
            distance_in_km = math.trunc(distance * 100)
            distance_dict[str(rd.title)] = distance_in_km


        return JsonResponse(distance_dict)

    @api_view(['GET'])
    def roadMapByCity(request,city):
        boto3.setup_default_session(region_name='us-east-2')
        s3_client = boto3.client('s3')
        roadMap = RoadMap.objects.filter(city_id__name=city)

        try:
            for point in roadMap:
                response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'bestridebucket',
                                                                'Key': '' + point.image},
                                                        ExpiresIn=3200)
                point.image = response
        except ClientError as e:
            logging.error(e)

        roadMapSerializer = RoadMapSerializer(roadMap,many=True)
        return Response(roadMapSerializer.data)

    @api_view(['GET'])
    def getPointsInterest(request):
        boto3.setup_default_session(region_name='us-east-2')
        s3_client = boto3.client('s3')
        Points = PointInterest.objects.all()

        try:
            for point in Points:
                response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'bestridebucket',
                                                                'Key': '' + point.image},
                                                        ExpiresIn=3200)
                point.image = response
        except ClientError as e:
            logging.error(e)

        Points_Serializer = InterestPointsSerializaer(Points,many=True)
        return Response(Points_Serializer.data)

    @api_view(['Post'])
    def postPointsInterest(request):
        pointInterestSerializer = InterestPointsSerializaer(data=request.data)
        if pointInterestSerializer.is_valid():
            pointInterestSerializer.save()
            emergencyContact_result = EmergencyContactDriverSerializer()
            return Response(emergencyContact_result.data, status=201)
        return Response(pointInterestSerializer.errors, status=400)

    @api_view(['GET'])
    def getPointsInterest(request):
        pointsInterest = PointInterest.objects.all()
        interestPointsSerializer = InterestPointsSerializaer(pointsInterest, many=True)
        return Response(pointsInterest.data)

    @api_view(['GET'])
    def getItineary(request,id):
        if id:
            Itineary = ItinearyRoute.objects.filter(road_map=id)
            boto3.setup_default_session(region_name='us-east-2')
            s3_client = boto3.client('s3')

            try:
                for ip in Itineary:
                    response = s3_client.generate_presigned_url('get_object',
                                                                Params={'Bucket': 'bestridebucket',
                                                                        'Key': '' + ip.interest_points.image},
                                                                ExpiresIn=3200)
                    ip.interest_points.image = response
            except ClientError as e:
                logging.error(e)


            Itineary_Serializer = ItinearyRouteSerializer(Itineary,many=True)
            return Response(Itineary_Serializer.data)
        else:
            return Response("ID missing")

    @api_view(['GET'])
    def getRoadVehicle(request,id):
        if id:
            roadVehicle = RoadVehicle.objects.all().filter(road_map=id)
            roadvehicleSerializer = RoadVehicleSerializer(roadVehicle,many=True)
            return Response(roadvehicleSerializer.data)
        else:
            return Response("ID Missing")

    @api_view(['GET'])
    def getVehicles(request):
        vehicles = Vehicle.objects.all()
        vehicleSerializer = VehicleSerializer(vehicles, many=True)
        return Response(vehicleSerializer.data)

    @api_view(['POST'])
    def postVehicle(request):
        roadVehicle_serializer = VehicleSerializer(data=request.data)
        if roadVehicle_serializer.is_valid():
            roadVehicle_serializer.save()
            roadVehicle_serializer = VehicleSerializer()
            return Response(roadVehicle_serializer.data, status=201)
        return Response(roadVehicle_serializer.errors, status=400)

    @api_view(['POST'])
    def postRoutes(request):
        route_serializer = RoadMapSerializer(data=request.data)
        if route_serializer.is_valid():
            route_serializer.save()
            route_result = RoadMapSerializer()
            return Response(route_result.data, status=201)
        return Response(route_serializer.errors, status=400)


