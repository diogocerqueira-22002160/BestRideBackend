import logging

from botocore.exceptions import ClientError
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework_gis.pagination import GeoJsonPagination
from django.contrib.gis.geos import Point
from environs import Env
import math
import urllib3


env = Env()
env.read_env()


import boto3


class user_operations(APIView):
    @api_view(['POST'])
    def recoverAccount(request):
        boto3.setup_default_session(region_name='eu-west-2')
        client = boto3.client('cognito-idp')

        try:
            response = client.forgot_password(
                ClientId=env.str("CLIENT_ID"),
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
                    ClientId=env.str("CLIENT_ID"),
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
                ClientId=env.str("CLIENT_ID"),
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
                ClientId=env.str("CLIENT_ID"),
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
                        'Name': "locale",
                        'Value': request.data['city']
                    },
                    {
                        'Name': "email",
                        'Value': request.data['email']
                    },
                    {
                        'Name': "address",
                        'Value': request.data['address']
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
    def changePassword(request,token):
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
        boto3.setup_default_session(region_name='us-west-2')
        client = boto3.client('cognito-idp')
        try:
            client.delete_user(
                AccessToken = request.data['token']
            )
            return Response("User eliminated !")
        except client.exceptions.UserNotFoundException:
            return Response("User Not Found", status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        boto3.setup_default_session(region_name=env.str('REGION_NAME_DEFAULT'))
        client = boto3.client('cognito-idp')
        try:
            response = client.sign_up(
                ClientId=env.str('CLIENT_ID'),
                Username=request.data['email'],
                Password=request.data['password'],
                UserAttributes=[
                    {
                        'Name': "name",
                        'Value': request.data['name']
                    },
                    {
                        'Name': "birthdate",
                        'Value': request.data['dob']
                    },
                    {
                        'Name': "email",
                        'Value': request.data['email']
                    },
                    {
                        'Name': "gender",
                        'Value': request.data['gender']
                    },
                    {
                        'Name': "address",
                        'Value': request.data['adress']
                    },
                    {
                        'Name': "locale",
                        'Value': request.data['city']
                    },
                    {
                        'Name': "phone_number",
                        'Value': request.data['phone_number']
                    },
                ],
            )
            return JsonResponse(response)

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
                ClientId=env.str('CLIENT_ID'),
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
        boto3.setup_default_session(region_name='eu-west-2')
        cidp = boto3.client('cognito-idp')
        response = cidp.get_id(
            AccountId='YOUR AWS ACCOUNT ID',
            IdentityPoolId='us-east-1:xxxdexxx-xxdx-xxxx-ac13-xxxxf645dxxx',
            Logins={
                'accounts.google.com': 'google returned IdToken'
            })

        return Response(response)






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

class Users(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @api_view(['GET'])
    def get(request,email):
        queryset = User.objects.all().filter(email=email)
        serializer_class = UserSerializer(queryset,many=True)
        return Response(serializer_class.data)

class Travels(generics.RetrieveDestroyAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    @api_view(['GET'])
    def get(request,turist_id):
        queryset = Travel.objects.all().filter(turist_id=turist_id)
        serializer_class = TravelSerializer(queryset,many=True)
        return Response(serializer_class.data)

    @api_view(['POST'])
    def post(request):
        travel_serializer = TravelSerializer(data=request.data)
        if travel_serializer.is_valid():
            travel = travel_serializer.save()
            travel_result = TravelSerializer(travel)
            return Response(travel_result.data, status=201)
        return Response(travel_serializer.errors, status=400)
