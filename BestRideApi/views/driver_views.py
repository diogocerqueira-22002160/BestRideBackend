from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from environs import Env
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from BestRideApi.serializers import *

env = Env()
env.read_env()

import boto3
boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))

class CognitoDriver():

    @api_view(['POST'])
    def recoverAccount(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        try:
            response = client.forgot_password(
                ClientId=env.str("Driver_CLIENT_ID"),
                Username=request.data['email'])
            return Response(response)
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def confirmRecoverAccount(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        try:
            response = client.confirm_forgot_password(
                    ClientId=env.str("Driver_CLIENT_ID"),
                    Username=request.data['email'],
                    ConfirmationCode=str(request.data['code']),
                    Password=request.data['password'],
            )
            return Response(response)
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def resend_code(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        try:
            response = client.resend_confirmation_code(
                ClientId=env.str("Driver_CLIENT_ID"),
                Username=request.data['email'])

            return JsonResponse(response)

        except client.exceptions.TooManyRequestsException:
            return Response("Too Many Requests", status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.LimitExceededException:
            return Response("Limit Exceeded", status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.InvalidEmailRoleAccessPolicyException:
            return Response("Invalid Email Role", status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.CodeDeliveryFailureException:
            return Response("Code not Delivered", status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def confirmAccount(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        cidp = boto3.client('cognito-idp')

        try:
            response_confirmUser = cidp.confirm_sign_up(
                ClientId=env.str("Driver_CLIENT_ID"),
                Username=request.data['email'],
                ConfirmationCode=request.data['code']
            )
            return Response(response_confirmUser)

        except cidp.exceptions.NotAuthorizedException:
            return Response("Not Authorized", status=status.HTTP_404_NOT_FOUND)
        except cidp.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)
        except cidp.exceptions.LimitExceededException:
            return Response("Limit has Exceeded", status=status.HTTP_404_NOT_FOUND)
        except cidp.exceptions.CodeMismatchException:
            return Response("Code Mismatch", status=status.HTTP_404_NOT_FOUND)
        except cidp.exceptions.ExpiredCodeException:
            return Response("Code had Expired", status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET'])
    def getUser(request, token):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        cidp = boto3.client('cognito-idp')

        try:
            response = cidp.get_user(
                AccessToken=token
            )

            return Response(response)
        except cidp.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)
        except cidp.exceptions.NotAuthorizedException:
            return Response("Wrong Acess Token", status=status.HTTP_404_NOT_FOUND)

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
                        'Name': "Name",
                        'Value': request.data['name']
                    },
                    {
                        'Name': "Birth",
                        'Value': request.data['dob']
                    },
                    {
                        'Name': "email",
                        'Value': request.data['email']
                    },
                    {
                        'Name': "Gender",
                        'Value': request.data['gender']
                    },
                    {
                        'Name': "Adress",
                        'Value': request.data['adress']
                    },
                    {
                        'Name': "City",
                        'Value': request.data['city']
                    },
                    {
                        'Name': "PostalCode",
                        'Value': request.data['PostalCode']
                    },
                    {
                        'Name': "Country",
                        'Value': request.data['Country']
                    },
                    {
                        'Name': "NIF",
                        'Value': request.data['NIF']
                    },
                    {
                        'Name': "RNATLicense",
                        'Value': request.data['RNATLicense']
                    },
                    {
                        'Name': "DriverLicense",
                        'Value': request.data['DriverLicense']
                    },
                    {
                        'Name': "Phone",
                        'Value': request.data['Phone']
                    },
                    {
                        'Name': "Nationality",
                        'Value': request.data['Nationality']
                    },
                    {
                        'Name': "CitizenCard",
                        'Value': request.data['CitizenCard']
                    },
                    {
                        'Name': "ANCATNumber",
                        'Value': request.data['ANCATNumber']
                    },
                    {
                        'Name': "IBAN",
                        'Value': request.data['IBAN']
                    },
                    {
                        'Name': "Image",
                        'Value': request.data['Image']
                    },
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

    @api_view(['PUT'])
    def updateUser(request, token):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        client = boto3.client('cognito-idp')

        try:
            response = client.update_user_attributes(
                UserAttributes=[
                    {
                        'Name': "Name",
                        'Value': request.data['name']
                    },
                    {
                        'Name': "Birth",
                        'Value': request.data['dob']
                    },
                    {
                        'Name': "email",
                        'Value': request.data['email']
                    },
                    {
                        'Name': "Gender",
                        'Value': request.data['gender']
                    },
                    {
                        'Name': "Adress",
                        'Value': request.data['adress']
                    },
                    {
                        'Name': "City",
                        'Value': request.data['city']
                    },
                    {
                        'Name': "PostalCode",
                        'Value': request.data['PostalCode']
                    },
                    {
                        'Name': "Country",
                        'Value': request.data['Country']
                    },
                    {
                        'Name': "NIF",
                        'Value': request.data['NIF']
                    },
                    {
                        'Name': "RNATLicense",
                        'Value': request.data['RNATLicense']
                    },
                    {
                        'Name': "DriverLicense",
                        'Value': request.data['DriverLicense']
                    },
                    {
                        'Name': "Phone",
                        'Value': request.data['Phone']
                    },
                    {
                        'Name': "Nationality",
                        'Value': request.data['Nationality']
                    },
                    {
                        'Name': "CitizenCard",
                        'Value': request.data['CitizenCard']
                    },
                    {
                        'Name': "ANCATNumber",
                        'Value': request.data['ANCATNumber']
                    },
                    {
                        'Name': "IBAN",
                        'Value': request.data['IBAN']
                    },
                    {
                        'Name': "Image",
                        'Value': request.data['Image']
                    },
                ],
                AccessToken='' + token,
            )
            return Response(response)
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.UserNotConfirmedException:
            return Response("Confirm your account!", status=status.HTTP_404_NOT_FOUND)

    @api_view(['PUT'])
    def changePassword(request, token):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        try:
            response = client.change_password(
                PreviousPassword=request.data['pass'],
                ProposedPassword=request.data['new_pass'],
                AccessToken=request.data['token']
            )

            return Response(response)
        except client.exceptions.InvalidPasswordException:
            return Response("Invalid Password", status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def saveUser(request):
        if request.method == 'POST':
            tutorial_data = JSONParser().parse(request)
            tutorial_serializer = UserSerializer(data=tutorial_data)
            if tutorial_serializer.is_valid():
                tutorial_serializer.save()
                return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['PUT'])
    def updateImageUser(request, email):
        tutorial = User.objects.get(email=email)
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = UserSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def cancelAccount(request):
        boto3.setup_default_session(region_name='us-west-2')
        client = boto3.client('cognito-idp')
        try:
            client.delete_user(
                AccessToken=request.data['token']
            )
            return Response("User eliminated !")
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def login(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        cidp = boto3.client('cognito-idp')
        try:
            login_request = cidp.initiate_auth(
                ClientId=env.str('Driver_CLIENT_ID'),
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    'USERNAME': request.data['email'],
                    'PASSWORD': request.data['password']
                }
            )

            return Response(login_request, status=status.HTTP_200_OK)

        except cidp.exceptions.NotAuthorizedException:
            return Response("Incorrect username or password", status=status.HTTP_404_NOT_FOUND)

    def loginGoogle(request):
        boto3.setup_default_session(region_name='eu-west-2')
        cidp = boto3.client('cognito-idp')
        response = cidp.get_id(
            AccountId='YOUR AWS ACCOUNT ID',
            IdentityPoolId='us-east-1:xxxdexxx-xxdx-xxxx-ac13-xxxxf645dxxx',
            Logins={
                'accounts.google.com': 'google returned IdToken'
            })

        return Response(response)

class ViewsDriver():
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
    def getDriver(request, email):
        queryset = Driver.objects.all().filter(email=email)
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