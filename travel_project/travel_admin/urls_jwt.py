from django.urls import path

# from .views import (WelcomeView, UserCreateAPIView, UserAPIView, 
#                     UserDetailByIdAPIView, 
#                     UserUpdateAPIView, UserDeleteAPIView, TravelPlanCreateAPIView, TravelPlanAPIView, TravelPlanDetailByIdAPIView,
#                     TravelPlanUpdateAPIView, TravelPlanDeleteAPIView, BookingsCreateAPIView, BookingsAPIView, BookingsDetailByIdAPIView,
#                     BookingsUpdateAPIView, BookingsDeleteAPIView)
from .views import UserAPI
from django.views.generic import TemplateView

urlpatterns = [
    # path('api/welcome/', WelcomeView.as_view(), name='welcome-api'),

    path('users/', UserAPI.as_view(), name='user-list-create'),
    path('users/<int:id>/', UserAPI.as_view(), name='user-detail-update-delete'),
    
    # path('api/users/create/', UserCreateAPIView.as_view(), name='user-create-api'),
    # path('api/users/', UserAPIView.as_view(), name='user-api'),
    # path('api/users/<int:id>/', UserDetailByIdAPIView.as_view(), name='user-detail-by-id-api'),
    # path('api/users/update/<int:id>/', UserUpdateAPIView.as_view(), name='user-update-api'),
    # path('api/users/delete/<int:id>/', UserDeleteAPIView.as_view(), name='user-delete-api'),


    # path('api/travelPlan/create/', TravelPlanCreateAPIView.as_view(), name='travelPlan-create-api'),
    # path('api/travelPlan/', TravelPlanAPIView.as_view(), name='travelPlan-api'),
    # path('api/travelPlan/<int:id>/', TravelPlanDetailByIdAPIView.as_view(), name='travelPlan-detail-by-id-api'),
    # path('api/travelPlan/update/<int:id>/', TravelPlanUpdateAPIView.as_view(), name='travelPlan-update-api'),
    # path('api/travelPlan/delete/<int:id>/', TravelPlanDeleteAPIView.as_view(), name='travelPlan-delete-api'),


    # path('api/Bookings/create/', BookingsCreateAPIView.as_view(), name='Bookings-create-api'),
    # path('api/Bookings/', BookingsAPIView.as_view(), name='Bookings-api'),
    # path('api/Bookings/<int:id>/', BookingsDetailByIdAPIView.as_view(), name='Bookings-detail-by-id-api'),
    # path('api/Bookings/update/<int:id>/', BookingsUpdateAPIView.as_view(), name='Bookings-update-api'),
    # path('api/Bookings/delete/<int:id>/', BookingsDeleteAPIView.as_view(), name='Bookings-delete-api'),

    # path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
]