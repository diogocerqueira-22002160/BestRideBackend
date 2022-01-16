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


class DriverEnterpriseCognito:
    @api_view(['POST'])
    def recoverAccount(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        client = boto3.client('cognito-idp')

        try:
            response = client.forgot_password(
                ClientId=env.str("DriverEnterprise_CLIENT_ID"),
                Username=request.data['email'])
            return Response(response)
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def confirmRecoverAccount(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        client = boto3.client('cognito-idp')

        try:
            response = client.confirm_forgot_password(
                    ClientId=env.str("DriverEnterprise_CLIENT_ID"),
                    Username=request.data['email'],
                    ConfirmationCode=str(request.data['code']),
                    Password=request.data['password'],
            )
            return Response(response)
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def resend_code(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        client = boto3.client('cognito-idp')

        try:
            response = client.resend_confirmation_code(
                ClientId=env.str("DriverEnterprise_CLIENT_ID"),
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
                ClientId=env.str("DriverEnterprise_CLIENT_ID"),
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
    def getUser(request,token):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        cidp = boto3.client('cognito-idp')

        try:
            response = cidp.get_user(
                AccessToken = token
            )

            return Response(response)
        except cidp.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)
        except cidp.exceptions.NotAuthorizedException:
            return Response("Wrong Acess Token", status=status.HTTP_404_NOT_FOUND)

    @api_view(['PUT'])
    def updateUser(request,token):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        client = boto3.client('cognito-idp')

        try:
            response = client.update_user_attributes(
                UserAttributes=[
                    {
                        'Name': "name",
                        'Value': request.data['name']
                    },
                    {
                        'Name': "address",
                        'Value': request.data['address']
                    },
                    {
                        'Name': "locale",
                        'Value': request.data['locale']
                    },
                    {
                        'Name': "Coutry",
                        'Value': request.data['coutry']
                    },
                    {
                        'Name': "PostalCode",
                        'Value': request.data['postalCode']
                    },
                    {
                        'Name': "NIF",
                        'Value': request.data['nif']
                    },
                    {
                        'Name': "phone_number",
                        'Value': request.data['phone_number']
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
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
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
    def updateImageUser(request,email):
        tutorial = User.objects.get(email=email)
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = UserSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def cancelAccount(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        client = boto3.client('cognito-idp')
        try:
            client.delete_user(
                AccessToken = request.data['token']
            )
            return Response("User eliminated !")
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def create_account(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        client = boto3.client('cognito-idp')
        try:
            response_sign_up = client.sign_up(
                ClientId=env.str('DriverEnterprise_CLIENT_ID'),
                Username=request.data['email'],
                Password=request.data['password'],
                UserAttributes=[
                    {
                        'Name': "name",
                        'Value': request.data['name']
                    },
                    {
                        'Name': "address",
                        'Value': request.data['address']
                    },
                    {
                        'Name': "locale",
                        'Value': request.data['locale']
                    },
                    {
                        'Name': "custom:country",
                        'Value': request.data['country']
                    },
                    {
                        'Name': "custom:postalcode",
                        'Value': request.data['postalcode']
                    },
                    {
                        'Name': "custom:nif",
                        'Value': request.data['nif']
                    },
                    {
                        'Name': "phone_number",
                        'Value': request.data['phone_number']
                    },
                ],
            )


            return JsonResponse(response_sign_up)

        except client.exceptions.InvalidPasswordException:
            return Response("Invalid Password Format",status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.UsernameExistsException:
            return Response("Username already Exists !", status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.CodeDeliveryFailureException:
            return Response("Error on send Code !", status=status.HTTP_404_NOT_FOUND)


    @api_view(['POST'])
    def login(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        cidp = boto3.client('cognito-idp')
        try:
            login_request = cidp.initiate_auth(
                ClientId=env.str('DriverEnterprise_CLIENT_ID'),
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    'USERNAME': request.data['email'],
                    'PASSWORD': request.data['password']
                }
            )

            return Response(login_request,status=status.HTTP_200_OK)

        except cidp.exceptions.NotAuthorizedException:
            return Response("Incorrect username or password",status=status.HTTP_404_NOT_FOUND)

    def loginGoogle(request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        cidp = boto3.client('cognito-idp')
        response = cidp.get_id(
            AccountId='YOUR AWS ACCOUNT ID',
            IdentityPoolId='us-east-1:xxxdexxx-xxdx-xxxx-ac13-xxxxf645dxxx',
            Logins={
                'accounts.google.com': 'google returned IdToken'
            })

        return Response(response)


class DriverEnterprise:
    @api_view(['POST'])
    def postDriverEmpresa(request):
        driver_serializer = EmpresaDriverSerializer(data=request.data)
        if driver_serializer.is_valid():
            driver_serializer.save()
            return Response(driver_serializer.data, status=201)
        return Response(driver_serializer.errors, status=400)

    @api_view(['GET'])
    def getDriverEmpresa(request):
        queryset = EmpresaDriver.objects.all()
        serialzer_class = EmpresaDriverSerializer(queryset, many=True)
        return Response(serialzer_class.data)

    @api_view(['GET'])
    def getDriverEmpresa(request, email):
        queryset = EmpresaDriver.objects.all().filter(email=email)
        serialzer_class = EmpresaDriverSerializer(queryset, many=True)
        return Response(serialzer_class.data)

    @api_view(['GET'])
    def delete(request,email):
        print(request)
        queryset = EmpresaDriver.objects.get(email=email)
        queryset.delete()
        return Response("User eliminado")