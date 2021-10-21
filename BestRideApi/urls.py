from django.urls import path
from .views import user_views,routes_views,views,travel_views,payments_views,comment_views
from . import driver_views

urlpatterns = [
    path('', views.api_root),
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
    path('translate/', views.TranslateAWS.translate),
    path('itineary/showItineary/<int:id>',routes_views.Routes.getItineary),
    path('showRoadMapsCity/<str:city>',routes_views.Routes.roadMapByCity),
    path('itineray/showRoadVehicles/<int:id>',routes_views.Routes.getRoadVehicle),
    path('itineary/showRoadMap',routes_views.Routes.getRoadMap),
    path('itineary/showInterestPoints',routes_views.Routes.getPointsInterest),
    path('itineary/distance/',routes_views.Routes.distance),
    path('getComments/<int:id>', comment_views.Comment.getComments),
    path('postComments/', comment_views.Comment.postComments),
    path('travelsSchedule/',travel_views.TravelScheduleList.as_view()),
    path('travelsSchedule/<int:pk>/',travel_views.TravelScheduleGet.get),
    path('travels/<int:turist_id>',travel_views.Travels.get),
    path('createTravel/',travel_views.Travels.post),
    path('getUserid/<str:email>/',user_views.Users.get),
    path('makePayment/',payments_views.Payments.make_payment),
    # Driver Urls
    path('create_driver/',driver_views.Driver.create_account)
]