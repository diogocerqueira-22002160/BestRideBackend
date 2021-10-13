from django.urls import path
from . import views
from . import payments_views
from . import driver_views

urlpatterns = [
    # Turist Urls
    path('users/', views.user_operations.as_view(),name='users'),
    path('login/',views.user_operations.login),
    path('getUser/<str:token>',views.user_operations.getUser),
    path('recoverUser/',views.user_operations.recoverAccount),
    path('updateUser/<str:token>',views.user_operations.updateUser),
    path('changePassword/<str:token>',views.user_operations.changePassword),
    path('saveUser/',views.user_operations.saveUser),
    path('updateImage/<str:email>',views.user_operations.updateImageUser),
    path('confirmRecoverUser/',views.user_operations.confirmRecoverAccount),
    path('verifyAccount/',views.user_operations.confirmAccount),
    path('resend_code/',views.user_operations.resend_code),
    path('cancelAccount/',views.user_operations.cancelAccount),
    path('users/<int:id>/', views.user_operations.as_view()),
    path('socialLogin/google/', views.user_operations.loginGoogle),
    path('translate/', views.TranslateAWS.translate),
    path('itineary/showItineary/<int:id>',views.Routes.getItineary),
    path('showRoadMapsCity/<str:city>',views.Routes.roadMapByCity),
    path('itineray/showRoadVehicles/<int:id>',views.Routes.getRoadVehicle),
    path('itineary/showRoadMap',views.Routes.getRoadMap),
    path('itineary/showInterestPoints',views.Routes.getPointsInterest),
    path('itineary/distance/',views.Routes.distance),
    path('getComments/<int:id>', views.Comment.getComments),
    path('postComments/', views.Comment.postComments),
    path('travelsSchedule/',views.TravelScheduleList.as_view()),
    path('travelsSchedule/<int:pk>/',views.TravelScheduleGet.get),
    path('travels/<int:turist_id>',views.Travels.get),
    path('createTravel/',views.Travels.post),
    path('getUserid/<str:email>/',views.Users.get),
    path('makePayment/',payments_views.Payments.make_payment),
    # Driver Urls
    path('create_driver/',driver_views.Driver.create_account)
]