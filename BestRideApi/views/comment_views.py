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


class Comment(APIView):

    @api_view(['POST'])
    def postComments(request):
        if request.method == 'POST':
            tutorial_data = JSONParser().parse(request)
            comment_serializer = CommentsSerializer(data=tutorial_data)

            if comment_serializer.is_valid():
                comment_item_object = comment_serializer.save()
                return JsonResponse(comment_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def getComments(request, id):
        comment = Comments.objects.all().filter(road_map=id)
        comments_Serializer = CommentsSerializer(comment, many=True)
        return Response(comments_Serializer.data)

