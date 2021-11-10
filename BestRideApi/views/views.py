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
import os

class Images:
    @api_view(['POST'])
    def upload_file(request):
        """
        file_name: File to upload
        bucket: Bucket to upload to
        object_name: S3 object name. If not specified then file_name is used
        return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if request.data['object_name'] is None:
            object_name = os.path.basename(request.data['file_name'])

        # Upload the file
        s3_client = boto3.client('s3')

        try:
            response = s3_client.upload_file(request.data['file_name'], request.data['bucket'], request.data['object_name'])
        except ClientError as e:
            logging.error(e)
            return False
        return True



class TranslateAWS():

    @api_view(['POST'])
    def translate(request):
        client = boto3.client('translate')
        response = client.translate_text(
            Text=request.data['text'], SourceLanguageCode=request.data['sourceLang'],
            TargetLanguageCode=request.data['outputLang'])

        return JsonResponse({
            "translated_text": response['TranslatedText']
        })

@api_view(['GET'])
def api_root(request, format=None):
    """
    API for Best Ride App
    """
    return Response({
        'Users': reverse('users', request=request, format=format),
    })
