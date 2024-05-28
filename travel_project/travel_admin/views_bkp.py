from rest_framework import generics, views
# from rest_framework.views import generics
from rest_framework.views import APIView
# from rest_framework.views import generics
from .models import User, TravelPlan, Bookings, BlacklistedAccessToken
from .serializers import UserSerializer, TravelPlanSerializer, BookingsSerializer, BookingsDetailsSerializer, UserDetailsWithBookingsSerializer, UserSerializer2
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
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


class HomeView(views.APIView):
    # content = ''
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)


class WelcomeView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "Welcome to the user API"}, status=status.HTTP_200_OK)

'''
class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        
        try:
            print("--> ",request.data.keys())
            print("--> ",request.data.values())
        #    print("--> ",request.data["refresh"])
            # Blacklist the refresh token
            refresh_token = request.data["refresh"]
            access_token = request.data["access"]
            access_token_obj = AccessToken(access_token)
            access_token_obj.blacklist()
            print("Access token is blacklisted")

            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.blacklist()
            print("refresh token is blacklisted")
            # Blacklist the access token
            
            msg = {"Message": "Success"}
            return Response(msg, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            msg = {"Message": "Error"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        
        # def post(self, request):
        try:
            refresh_token = request.data.get("refresh") # Expire
            print("***: ",request.data.get("refresh"))
            if refresh_token is None:
                return Response({"Message": "Refresh token is missing."}, status=status.HTTP_400_BAD_REQUEST)

            # Attempt to blacklist the refresh token
            try:
                refresh_token_obj = RefreshToken(refresh_token)
                refresh_token_obj.blacklist()
            except TokenError as e:
                return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"Message": "Success"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"Message": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # def post(self, request):
        #   tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        #   for token in tokens:
        #     t, _ = BlacklistedToken.objects.get_or_create(token=token)

        #   return Response(status=status.HTTP_205_RESET_CONTENT)

'''
class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''
class UserCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Manually create and save the user object
            user = serializer.save()
            # Customize any additional processing here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

# class UserAPIView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, format=None):
            # print("--> ", request.user)
            # if request.user.is_superuser:
            '''
                print("Request content: ", request)
                queryset = User.objects.all()
                serializer = UserSerializer(queryset, many=True)
                print("------------------")
                print(serializer.data)
                print("------------------")
                return Response(serializer.data)
            '''
            if request.user.is_authenticated and request.user.is_admin:  # Check if the user is authenticated and is admin
                queryset = User.objects.all()
                serializer = UserSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Permission denied."}, status=403)  # Return forbidden status for non-admin users
            # else:
            #     return Response({"Message": "Permission Denied"}, status=403)

class UserDetailByIdAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer
'''
class UserDetailByIdAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)
'''
class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer
'''
class UserUpdateAPIView(APIView):
    def put(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
class UserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer
'''
class UserDeleteAPIView(APIView):
    def delete(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
'''

class UserAPIView(APIView):
    def get(self, request, id=None, format=None):
        if id:
            # Retrieve a single user
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all users
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
'''
URLS

urlpatterns = [
    path('users/', UserAPIView.as_view(), name='user-list'),
    path('users/<int:id>/', UserAPIView.as_view(), name='user-detail'),
]
'''

# Travel Plan APIs

class TravelPlanCreateAPIView(generics.CreateAPIView):
    queryset = TravelPlan.objects.all()
    serializer_class = TravelPlanSerializer
    permission_classes = [IsAuthenticated]

class TravelPlanAPIView(generics.ListAPIView):
    queryset = TravelPlan.objects.all()
    serializer_class = TravelPlanSerializer
    permission_classes = [IsAuthenticated]

class TravelPlanDetailByIdAPIView(generics.RetrieveAPIView):
    queryset = TravelPlan.objects.all()
    lookup_field = 'id'
    serializer_class = TravelPlanSerializer
    permission_classes = [IsAuthenticated]

class TravelPlanUpdateAPIView(generics.UpdateAPIView):
    queryset = TravelPlan.objects.all()
    lookup_field = 'id'
    serializer_class = TravelPlanSerializer
    permission_classes = [IsAuthenticated]

class TravelPlanDeleteAPIView(generics.DestroyAPIView):
    queryset = TravelPlan.objects.all()
    lookup_field = 'id'
    serializer_class = TravelPlanSerializer
    permission_classes = [IsAuthenticated]



# Booking Plan APIs

class BookingsCreateAPIView(generics.CreateAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated]

class BookingsAPIView(generics.ListAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated]

class BookingsDetailByIdAPIView(generics.RetrieveAPIView):
    queryset = Bookings.objects.all()
    lookup_field = 'id'
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated]


class BookingsUpdateAPIView(generics.UpdateAPIView):
    queryset = Bookings.objects.all()
    lookup_field = 'id'
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated]

class BookingsDeleteAPIView(generics.DestroyAPIView):
    queryset = Bookings.objects.all()
    lookup_field = 'id'
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated]

# User helper API

class BookingsDetailByUserIdAPIView(generics.ListAPIView):
    # queryset = Bookings.objects.filter(user_id=id')
    # queryset = Bookings.objects.all()
    serializer_class = BookingsDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['id']  # Get the user ID from URL kwargs
        return Bookings.objects.filter(user_id=user_id)
        # return Bookings.objects.select_related('travel_plan_id').filter(user_id=user_id)


class UserDetailWithBokings(views.APIView):
    permission_classes = (IsAuthenticated,)
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



