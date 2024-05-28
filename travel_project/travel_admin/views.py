from rest_framework import generics, views
# from rest_framework.views import generics
from rest_framework.views import APIView
# from rest_framework.views import generics
from .models import User, TravelPlan, Bookings, BlacklistedAccessToken
from .serializers import UserProfileBookingSerializer, BookingSerializer, UserSerializer, TravelPlanSerializer, BookingsSerializer, BookingsDetailsSerializer, UserDetailsWithBookingsSerializer, UserSerializer2
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth import logout
# This parameter will be added to each view that requires JWT authentication
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, OutstandingToken, BlacklistedToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from travel_admin.renderers import UserRenderer
from travel_admin.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework import views, permissions

logger = logging.getLogger(__name__)

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

# change password

from django.contrib.auth import get_user_model
from .serializers import ChangePasswordSerializer

User = get_user_model()

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    print(f"-> email: {email}, password: {password}")
    user = authenticate(email=email, password=password)
    print(f"User is **: ", user)
    if user is not None:
        token = get_tokens_for_user(user)
        
        if user.is_admin:  # Assuming is_admin is a boolean field in your user model
            return Response({'token': token, 'msg': 'Admin Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'token': token, 'msg': 'User Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    print("---> :", request.user)
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            access_token = request.data.get("access")
            
            # Blacklist refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Blacklist access token
            BlacklistedAccessToken.objects.create(token=access_token)

            # Log out the user from the session
            logout(request)

            return Response({'message': 'Logged out successfully'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)





# See all users by admin
class UsersAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    def get(self, request, format=None):

            if request.user.is_authenticated and request.user.is_admin:  # Check if the user is authenticated and is admin
                queryset = User.objects.all()
                serializer = UserSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Permission denied."}, status=403)  # Return forbidden status for non-admin users
            # else:
            #     return Response({"Message": "Permission Denied"}, status=403)






class NonAdminUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_admin


class BookingDetailsView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated, NonAdminUserPermission]
  def get(self, request, format=None):
    print("---> :", request.user)
    if not request.user.is_admin:
        id = request.user.id
        bookings = Bookings.objects.filter(user_id=id)
        print("****: ", bookings)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


'''
class BookingView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, plan_id, format=None):
    print("---> :", request.user)
    if not request.user.is_admin:
        id = request.user.id
        print("___>: ", request)
        obj = {"usaer_id": id, "travel_plan_id": plan_id}
        bookings = Bookings.objects.create(**obj)
        print("****: ", bookings)
        serializer = BookingSerializer(bookings)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
'''

    
# To create a new booking for a user: api/user/booking/<int:plan_id>
# class BookingView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated, NonAdminUserPermission]
#     renderer_classes = [UserRenderer]
#     def post(self, request, plan_id, format=None):
#         try:
#             # t = TravelPlan.objects.all()
#             # t = TravelPlan.objects.all()
#             # print("hello")
#             # serializer = TravelPlanSerializer(data = t, many=True)
#             # print("**: ", serializer.data)
#             travel_plan = TravelPlan.objects.get(pk=plan_id)
#             print("--> : ", TravelPlan.objects.all())
#             if travel_plan:
#                 serializer = BookingsSerializer(data = {"travel_plan": plan_id, "user_id": request.user.id})
               
#                 if serializer.is_valid():
#                     print("yyyy")
#                     serializer.save()
#                     return Response(serializer.data, status=201)  # Return success response with created booking data
#             return Response({"message": f"Travel plan does not exist."}, status=404)

#         except Exception as e:
#             return Response({"message": f"Travel plan does not exist. {e}"}, status=404)

#         # Create a new booking
#         # booking_data = {'user_id': request.user.id, 'travel_plan_id': travel_plan.id}
#         # serializer = BookingsSerializer(data=booking_data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data, status=201)  # Return success response with created booking data
#         # return Response(serializer.errors, status=400)  # Return error response if serializer is not valid
#         # return Response({'Message': "cool"})

class BookingView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, NonAdminUserPermission]
    renderer_classes = [UserRenderer]

    def post(self, request, plan_id, format=None):
        try:
            travel_plan = TravelPlan.objects.get(pk=plan_id)
            if travel_plan:
                data = {
                    "travel_plan_id": travel_plan.id,  # Ensure correct reference to the ID
                    "user_id": request.user.id
                }
                serializer = BookingsSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            return Response({"message": "Travel plan does not exist."}, status=404)
        except TravelPlan.DoesNotExist:
            return Response({"message": "Travel plan does not exist."}, status=404)
        except Exception as e:
            return Response({"message": f"An error occurred: {e}"}, status=500)
        
class BookingDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, NonAdminUserPermission]
    renderer_classes = [UserRenderer]

    def delete(self, request, booking_id, format=None):
        try:
            # Retrieve the existing booking object by booking_id
            booking = Bookings.objects.get(pk=booking_id, user_id=request.user.id)
        except Bookings.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the booking object
        booking.delete()
        
        return Response({'message': 'Booking deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class BookingEditView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, NonAdminUserPermission]
    renderer_classes = [UserRenderer]

    def put(self, request, booking_id, format=None):
        try:
            # Retrieve the existing booking object by booking_id
            booking = Bookings.objects.get(pk=booking_id, user_id=request.user.id)
        except Bookings.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the existing booking object with the updated data from request
        serializer = BookingsSerializer(booking, data=request.data)

        # Validate and save the serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return success response with updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error response if serializer is not valid


# # To create a new travel plan by Admin: api/travel_plan/
class TravelPlanView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):

        serializer = TravelPlanSerializer(data=request.data)
        
        if serializer.is_valid():
            print("---> ", serializer.validated_data)
            serializer.save()
            t= TravelPlan.objects.all()
            print(t)
            return Response(serializer.data, status=201)  # Return success response with created booking data
        return Response(serializer.errors, status=400)  # Return error response if serializer is not valid
    
class TravelPlanUpdateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    renderer_classes = [UserRenderer]

    def put(self, request, plan_id, format=None):
        try:
            # Retrieve the existing travel plan object by pk
            travel_plan = TravelPlan.objects.get(pk=plan_id)
        except TravelPlan.DoesNotExist:
            return Response({'error': 'Travel plan not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the existing travel plan object with the updated data from request
        serializer = TravelPlanSerializer(travel_plan, data=request.data)

        # Validate and save the serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return success response with updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error response if serializer is not valid
    
class TravelPlanDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    renderer_classes = [UserRenderer]

    def delete(self, request, plan_id, format=None):
        try:
            # Retrieve the existing travel plan object by pk
            travel_plan = TravelPlan.objects.get(pk=plan_id)
        except TravelPlan.DoesNotExist:
            return Response({'error': 'Travel plan not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the travel plan object
        travel_plan.delete()
        
        return Response({'message': 'Travel plan deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# # To create a new travel plan by Admin: api/travel_plan/
class TravelPlanGetView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]
    '''
    def get(self, request, format=None):
        # Create a new booking
        t= TravelPlan.objects.all()
        print("-->: ", t)
        serializer = TravelPlanSerializer(data = t, many=True)
        print(serializer.initial_data)
        if serializer.is_valid():

            return Response(serializer.data, status=201)  # Return success response with created booking data
        else:
            return Response(serializer.errors, status=400)  # Return error response if serializer is not valid
        
    '''

    # True to use user renderers
    def get(self, request, format=None):
        # Retrieve all travel plans
        travel_plans = TravelPlan.objects.all()

        # Serialize the queryset directly
        serializer = TravelPlanSerializer(travel_plans, many=True)

        # Check if serializer is valid
        
        return Response(serializer.data, status=200)  # Return success response with travel plans data
        # else:
        #     return Response(serializer.errors, status=400)  # Return error response if serializer is not valid



# class UserDetailsWithBooking(views.APIView):
#     permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
#     renderer_classes = [UserRenderer]
#     def get(self, request, format=None):

#         UserDetailsWithBookingsSerializer


class UserDetailWithBokings(views.APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer2(users, many=True)
        # filtered_data = {}
        # for data in serializer.data:
        #     for key in serializer.data[data]:
        #         filtered_data['id'] = serializer.data[data][key]['id']
        #         filtered_data['name'] = serializer.data[data][key]['name']
        #         filtered_data['email'] = serializer.data[data][key]['email']
                
        #         filtered_data['bookings'] = []
        #         for booking in serializer.data[data][key]['bookings']:
        #             for key1 in booking:
        #                 book = [booking[key1]['destination'], booking[key1]['cost'], booking[key1]['description']]
        #                 filtered_data['bookings'].append(book)
        return Response(serializer.data)
        # return Response(filtered_data)



class IndividualUserDetailWithBokings(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user_bookings = Bookings.objects.filter(user_id=request.user.id)
        serializer = UserProfileBookingSerializer(user_bookings, many=True)

        return Response(serializer.data)


