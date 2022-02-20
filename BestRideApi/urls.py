from django.urls import path
from .views import user_views, routes_views, views, travel_views, payments_views, comment_views, driver_views, \
    driverEnterprise_views

urlpatterns = [
    path('', views.api_root),

    #User Cognito Urls
    path('users/', user_views.user_operations.as_view(),name='users'),
    path('login/',user_views.user_operations.login),
    path('getUser/<str:token>',user_views.user_operations.getUser),
    path('recoverUser/',user_views.user_operations.recoverAccount),
    path('updateUser/<str:token>',user_views.user_operations.updateUser),
    path('changePassword/<str:token>',user_views.user_operations.changePassword),
    path('saveUser/',user_views.user_operations.saveUser),
    path('updateImage/<str:email>',user_views.user_operations.updateImageUser),
    path('confirmRecoverUser/',user_views.user_operations.confirmRecoverAccount),
    path('verifyAccount/',user_views.user_operations.confirmAccount),
    path('resend_code/',user_views.user_operations.resend_code),
    path('cancelAccount/',user_views.user_operations.cancelAccount),
    path('users/<int:id>/', user_views.user_operations.as_view()),
    path('socialLogin/google/', user_views.user_operations.loginGoogle),

    #User RDS Urls
    path('deleteUser/<int:id>', user_views.Users.delete),
    path('getUserid/<str:email>/',user_views.Users.get),

    #Translate Url
    path('translate/', views.TranslateAWS.translate),

    #Iteneary Urls
    path('itineary/showItineary/<int:id>',routes_views.Routes.getItineary),
    path('itineray/showRoadVehicles/<int:id>',routes_views.Routes.getRoadVehicle),
    path('itineary/showRoadMap',routes_views.Routes.getRoadMap),
    path('itineary/showInterestPoints',routes_views.Routes.getPointsInterest),
    path('itineary/distance/',routes_views.Routes.distance),

    #RoadMaps/Roteiros Urls
    path('showRoadMapsCity/<str:city>',routes_views.Routes.roadMapByCity),
    path('getRoadMapsByEnterprise/<int:enterprise>', routes_views.Routes.roadMapByEnterprise),
    path('getRoadMapsById/<int:id>', routes_views.Routes.roadMapById),
    path('createRoute/', routes_views.Routes.postRoutes),
    path('deleteRoute/<int:id>', routes_views.Routes.delete),
    path('updateRoadMap/<int:id>', routes_views.Routes.updateRoadMap),

    #Vehicle Urls
    path('getVehicle', routes_views.Routes.getVehicles),
    path('postVehicle', routes_views.Routes.postVehicle),
    path('deleteVehicle/<int:id>',  routes_views.Routes.deleteVehicle),
    path('getVehicleByEnterprise/<int:enterprise>', routes_views.Routes.getVehiclesEnterprise),
    path('getVehicleById/<int:id>', routes_views.Routes.getVehiclesId),
    path('updateVehicle/<int:id>', routes_views.Routes.updateVehicle),

    #Comments Urls
    path('getComments/<int:id>', comment_views.Comment.getComments),
    path('postComments/', comment_views.Comment.postComments),
    path('getAverageComments/<int:id>', comment_views.Comment.getAverageComments),

    #Travel Urls
    path('travelsSchedule/',travel_views.TravelScheduleList.as_view()),
    path('travelsSchedule/<int:pk>/',travel_views.TravelScheduleGet.get),
    path('travels/<int:turist_id>',travel_views.Travels.getTurista),
    path('getTravels/',travel_views.Travels.get),
    path('createTravel/',travel_views.Travels.post),

    #Point of Interest Urls
    path('createPointInterest/',routes_views.Routes.postPointsInterest),
    path('getPointInterest/',routes_views.Routes.getPointsInterest),

    #Payment Urls
    path('makePayment/',payments_views.Payments.make_payment),

    #Image Urls
    path('uploadImage/',views.Images.upload_file),

    # Driver Cognito Urls
    path('loginDriver/', driver_views.CognitoDriver.login),
    path('loginGoogleDriver/', driver_views.CognitoDriver.loginGoogle),
    path('cancelAccountDriver/', driver_views.CognitoDriver.cancelAccount),
    path('createDriver/', driver_views.CognitoDriver.create_account),
    path('getCognitoDriver/<str:token>',driver_views.CognitoDriver.getUser),
    path('recoverDriver/',driver_views.CognitoDriver.recoverAccount),
    path('updateDriver/<str:token>',driver_views.CognitoDriver.updateUser),
    path('changePasswordDriver/<str:token>',driver_views.CognitoDriver.changePassword),
    path('saveDriver/',driver_views.CognitoDriver.saveUser),
    path('updateImageDriver/<str:email>',driver_views.CognitoDriver.updateImageUser),
    path('confirmRecoverDriver/',driver_views.CognitoDriver.confirmRecoverAccount),
    path('verifyAccountDriver/',driver_views.CognitoDriver.confirmAccount),
    path('resend_codeDriver/',driver_views.CognitoDriver.resend_code),
    path('cancelAccountDriver/',driver_views.CognitoDriver.cancelAccount),

    # Driver RDS Urls
    path('getDriver/<str:email>', driver_views.ViewsDriver.getDriver),
    path('deleteDriver/<int:id>',  driver_views.ViewsDriver.delete),
    path('postEmergencyContact/', driver_views.ViewsDriver.postEmergencycontact),

    #Driver/Enterprise FK Urls
    path('postFKDriverEnterprise/', driver_views.ViewsDriver.postFkDrivertoEnterprise),
    path('getFKDriverEnterprise', driver_views.ViewsDriver.getFkDrivertoEnterprise),

    # Driver Enterprise Cognito Urls
    path('loginEnterprise/', driverEnterprise_views.DriverEnterpriseCognito.login),
    path('loginGoogleDriverEnterprise/', driverEnterprise_views.DriverEnterpriseCognito.loginGoogle),
    path('cancelAccountDriverEnterprise/', driverEnterprise_views.DriverEnterpriseCognito.cancelAccount),
    path('createDriverEnterprise/', driverEnterprise_views.DriverEnterpriseCognito.create_account),
    path('getCognitoDriverEnterprise/<str:token>',driverEnterprise_views.DriverEnterpriseCognito.getUser),
    path('recoverDriverEnterprise/',driverEnterprise_views.DriverEnterpriseCognito.recoverAccount),
    path('updateDriverEnterprise/<str:token>',driverEnterprise_views.DriverEnterpriseCognito.updateUser),
    path('changePasswordDriverEnterprise/<str:token>',driverEnterprise_views.DriverEnterpriseCognito.changePassword),
    path('saveDriverEnterprise/',driverEnterprise_views.DriverEnterpriseCognito.saveUser),
    path('updateImageDriverEnterprise/<str:email>',driverEnterprise_views.DriverEnterpriseCognito.updateImageUser),
    path('confirmRecoverDriverEnterprise/',driverEnterprise_views.DriverEnterpriseCognito.confirmRecoverAccount),
    path('verifyAccountDriverEnterprise/',driverEnterprise_views.DriverEnterpriseCognito.confirmAccount),
    path('resend_codeDriverEnterprise/',driverEnterprise_views.DriverEnterpriseCognito.resend_code),
    path('cancelAccountDriverEnterprise/',driverEnterprise_views.DriverEnterpriseCognito.cancelAccount),

    # Driver RDS Cognito Urls
    path('getEmpresa/',  driverEnterprise_views.DriverEnterprise.getDriverEmpresa),
    path('getEmpresaId/<str:email>',  driverEnterprise_views.DriverEnterprise.getDriverEmpresa),
    path('deleteEmpresa/<int:id>',  driverEnterprise_views.DriverEnterprise.delete),
]