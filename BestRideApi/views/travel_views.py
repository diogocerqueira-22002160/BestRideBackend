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


class TravelScheduleList(generics.ListCreateAPIView):
    queryset = TravelSchedule.objects.all()
    serializer_class = TravelScheduleSerializer

class TravelScheduleGet(generics.RetrieveDestroyAPIView):
    queryset = TravelSchedule.objects.all()
    serializer_class = TravelScheduleSerializer

    @api_view(['GET'])
    def get(request,pk):
        queryset = TravelSchedule.objects.all().filter(turist_id=pk)
        serializer_class = TravelScheduleSerializer(queryset,many=True)
        return Response(serializer_class.data)



class Travels(generics.RetrieveDestroyAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    @api_view(['GET'])
    def getTurista(request,turist_id):
        queryset = Travel.objects.all().filter(turist_id=turist_id)
        serializer_class = TravelSerializer(queryset,many=True)
        return Response(serializer_class.data)

    @api_view(['GET'])
    def get(request):
        queryset = Travel.objects.all()
        serializer_class = TravelSerializer(queryset, many=True)
        return Response(serializer_class.data)

    @api_view(['POST'])
    def post(request):
        travel_serializer = TravelSerializer(data=request.data)
        if travel_serializer.is_valid():
            travel_serializer.save()
            travel_result = TravelSerializer()
            return Response(travel_result.data, status=201)
        return Response(travel_serializer.errors, status=400)

