from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from environs import Env
from rest_framework.response import Response
from BestRideApi.serializers import *

env = Env()
env.read_env()

import boto3
boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))

class ViewsDriver():

    @api_view(['POST'])
    def create_account(request):
        client = boto3.client('cognito-idp')
        try:
            response_sign_up = client.sign_up(
                ClientId=env.str('Driver_CLIENT_ID'),
                Username=request.data['email'],
                Password=request.data['password'],
                UserAttributes=[
                    {
                        'Name': "email",
                        'Value': request.data['email']
                    }
                ],
            )

            response_confirm = client.admin_confirm_sign_up(
                UserPoolId=env.str('USER_POOL_ID'),
                Username=request.data['email'],
            )

            response_login = client.initiate_auth(
                ClientId=env.str("Driver_CLIENT_ID"),
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": request.data['email'],
                    "PASSWORD": request.data['password']
                },
            )
            return JsonResponse(response_login)

        except client.exceptions.InvalidPasswordException:
            return Response("Invalid Password Format",status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.UsernameExistsException:
            return Response("Username already Exists !", status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.CodeDeliveryFailureException:
            return Response("Error on send Code !", status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def postDriverEmpresa(request):
        driver_serializer = EmpresaDriverSerializer(data=request.data)
        if driver_serializer.is_valid():
            driver_serializer.save()
            driver_result = EmpresaDriverSerializer()
            return  Response(driver_result.data, status=201)
        return Response(driver_serializer.errors, status=400)

    @api_view(['GET'])
    def getDriverEmpresa(request):
        queryset = EmpresaDriver.objects.all()
        serialzer_class = EmpresaDriverSerializer(queryset, many=True)
        return Response(serialzer_class.data)

    @api_view(['POST'])
    def postDriver(request):
        driver_serializer = DriverSerializer(data=request.data)
        if driver_serializer.is_valid():
            driver_serializer.save()
            driver_result = DriverSerializer()
            return  Response(driver_result.data, status=201)
        return Response(driver_serializer.errors, status=400)

    @api_view(['GET'])
    def getDriver(request):
        queryset = Driver.objects.all()
        serialzer_class = DriverSerializer(queryset, many=True)
        return Response(serialzer_class.data)

    @api_view(['POST'])
    def postEmergencycontact(request):
        emergencyContact_serializer = EmergencyContactDriverSerializer(data=request.data)
        if emergencyContact_serializer.is_valid():
            emergencyContact_serializer.save()
            emergencyContact_result = EmergencyContactDriverSerializer()
            return Response(emergencyContact_result.data, status=201)
        return Response(emergencyContact_serializer.errors, status=400)