from django.urls import path

from .views import (UserRegistrationView)
# from .views import UserAPI
from django.views.generic import TemplateView
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    
    path('api/users/', UsersAPIView.as_view(), name='Admin-see-all-user'), # see all users details
    path('api/user/bookings/', BookingDetailsView.as_view(), name='User-Bookings'), # bookings of current user none admin

    path('api/user/booking_edit/<int:booking_id>/', BookingEditView.as_view(), name='User-Bookings'), # to edit a booking made by user by user
    path('api/user/booking_delete/<int:booking_id>/', BookingDeleteView.as_view(), name='User-Bookings'), # to delete booking

    path('api/user/booking/<int:plan_id>', BookingView.as_view(), name='User-Plan-Booking'), # Post request to create new booking for the ucrrent user for the given plan id, response {id, user_id, travel_plan_id}
    path('api/travel_plan/', TravelPlanView.as_view(), name='Admin-Plan-Creation'), # create a new travel plan by admin {cost, descirption, destination}
    path('api/travel_plan_edit/<int:plan_id>/', TravelPlanUpdateView.as_view(), name='Admin-Plan-Edit'), # edit travel plan by admin
    path('api/travel_plan_delete/<int:plan_id>/', TravelPlanDeleteView.as_view(), name='Admin-Plan-Delete'), # deelte ttravel plan by admin

    path('api/get_travel_plan/', TravelPlanGetView.as_view(), name='User_and_Admin_both-Plan-View'), # get all travel plan

    path('api/users_details/bookings/', UserDetailWithBokings.as_view(), name='Admin-users-details with-Bookings-View'), # get the all the user details with their booking sdetails  like this [{"id":1,"name":"admin","email":"admin@gmail.com","password":"pbkdf2_sha256$600000$FnWlhV6B7QlgEnNzGDCS2k$i2qQYRrqqaizHc9YfcZWAKYT+VimvfLlz0ZVYicrufI=","bookings":[]},{"id":2,"name":"user","email":"user@gmail.com","password":"pbkdf2_sha256$600000$gOIAEg6ZMgFxvBAXcj7nLB$ZIWif85scmoG8rBeyKbYy6dtFTyb1trsjbrydZozStg=","bookings":[{"id":1,"user_id":2,"travel_plan":{"id":4,"destination":"d1","cost":1,"description":"d1"}}]},{"id":3,"name":"name","email":"user1@gmail.com","password":"pbkdf2_sha256$600000$rdJ2vvyuVjpiKQ4bxQrCTc$ZnNp579goYRfIO++3GXxZNv61Nsoi50Oja7LOuf+oRM=","bookings":[{"id":2,"user_id":3,"travel_plan":{"id":4,"destination":"d1","cost":1,"description":"d1"}}]}]
    path('api/user/booking_with_travel_plan/', IndividualUserDetailWithBokings.as_view(), name='User-Bookings-View'), # Booking for the user logged in like this [{"id":1,"travel_plan":{"id":4,"destination":"d1","cost":1,"description":"d1"}}]
    
    path('api/register/', UserRegistrationView.as_view(), name='User-register'), # accept email, name, password, password2 return {"token": {"refresh": <refresh token>, "access token": <access token>}, "msg": "Registration success"}
    path('api/login/', UserLoginView.as_view(), name='user_and_admin_login'), # Login  accept email and password: return {"token": {"refresh": <refresh token>, "access token": <access token>}, "msg": "Admin Login Success or User Login Success"}
    path('api/user/profile/', UserProfileView.as_view(), name='user-profile'), # Shows the profile of current user {"id": <id>, "name": <name>, "email": <email>}
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/logout/', LogoutView.as_view(), name='user_and_admin_logout'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/logout/', views.LogoutView.as_view(), name ='logout'),
    

]