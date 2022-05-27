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
    def roadMapByEnterprise(request, enterprise):
        roadMap = RoadMap.objects.all().filter(enterprise=enterprise)
        roadMapSerializer = RoadMapSerializer(roadMap, many=True)
        return Response(roadMapSerializer.data)

    @api_view(['GET'])
    def roadMapById(request, id):
        roadMap = RoadMap.objects.all().filter(id=id)
        roadMapSerializer = RoadMapSerializer(roadMap, many=True)
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
            return Response(pointInterestSerializer.data, status=201)
        return Response(pointInterestSerializer.errors, status=400)

    @api_view(['GET'])
    def getPointsInterest(request):
        pointsInterest = PointInterest.objects.all()
        interestPointsSerializer = InterestPointsSerializaer(pointsInterest, many=True)
        return Response(pointsInterest.data)

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
            return Response(roadVehicle_serializer.data, status=201)
        return Response(roadVehicle_serializer.errors, status=400)

    @api_view(['DELETE'])
    def deleteVehicle(request, id):
        queryset = Vehicle.objects.get(id=id)
        queryset.delete()
        return Response("User eliminado")

    @api_view(['PUT'])
    def updateVehicle(request, id):
        Vehicle.objects.get(id=id).delete()
        roadVehicle_serializer = VehicleSerializer(data=request.data)
        if roadVehicle_serializer.is_valid():
            roadVehicle_serializer.save()
            return Response(roadVehicle_serializer.data, status=201)
        return Response(roadVehicle_serializer.errors, status=400)

    @api_view(['GET'])
    def getVehiclesId(request, id):
        vehicles = Vehicle.objects.all().filter(id=id)
        vehicleSerializer = VehicleSerializer(vehicles, many=True)
        return Response(vehicleSerializer.data)

    @api_view(['GET'])
    def getVehiclesEnterprise(request, enterprise):
        vehicles = Vehicle.objects.all().filter(enterprise=enterprise)
        vehicleSerializer = VehicleSerializer(vehicles, many=True)
        return Response(vehicleSerializer.data)

    @api_view(['POST'])
    def postRoutes(request):
        route_serializer = RoadMapSerializer(data=request.data)
        if route_serializer.is_valid():
            route_serializer.save()
            return Response(route_serializer.data, status=201)
        return Response(route_serializer.errors, status=400)

    @api_view(['DELETE'])
    def delete(request, id):
        queryset = RoadMap.objects.get(id=id)
        queryset.delete()
        return Response("Roteiro eliminado")

    @api_view(['PUT'])
    def saveDraft(request, id):
        tutorial = RoadMap.objects.get(id=id)
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = RoadMapSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['PUT'])
    def updateDriverVehicle(request, id):
        tutorial = Vehicle.objects.get(id=id)
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = VehicleSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

