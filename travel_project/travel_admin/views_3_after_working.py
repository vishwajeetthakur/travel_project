from rest_framework import generics, views
from .models import User, TravelPlan, Bookings
from .serializers import UserSerializer, TravelPlanSerializer, BookingsSerializer, BookingsDetailsSerializer
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
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)
# class PatchLogoutView(LogoutView):
#     http_method_names = ["get", "post", "options", "get"]
#     def get(self, request, *args, **kwargs):
#         # logout(request)
#         return self.post(request, *args, **kwargs)
def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )

class WelcomeView(views.APIView):
    def get(self, request):
        return Response({"message": "Welcome to the user API"}, status=status.HTTP_200_OK)

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]  # Only allow authenticated users to log out
    authentication_classes = (BasicAuthentication,)
    def get(self, request):
        # Clear the session to log out the user
        logger.warning(f"This is logging before request content: {pretty_request(request)}")
        logout(request)
        logger.warning(f"This is logging after request content: {pretty_request(request)}")
        # logger.warning(f"This is logging request content: {request.keys()}")
        # return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        # Create a response with a 401 Unauthorized status.
        # response = HttpResponse("You are logged out.", status=401)
        # Add the WWW-Authenticate header to the response.
        # response['WWW-Authenticate'] = 'Basic realm="Login Required"'
        return HttpResponse("You are logged out.", status=201)



# class UserCreateAPIView(generics.CreateAPIView):

#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (BasicAuthentication,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserCreateAPIView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]  # Change to JWTAuthentication if you use JWT
    # authentication_classes = [JWTAuthentication]  # Change to JWTAuthentication if you use JWT
    queryset = User.objects.all()
    serializer_class = UserSerializer
    '''
    def post(self, request, *args, **kwargs):
        # Extract the JWT token from the Authorization header (if available)
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            jwt_token = auth_header.split(' ')[1]
        else:
            jwt_token = 'No JWT token provided'

        # Print the request content and JWT token
        logger.warning("Request data:", request.data)
        logger.warning("JWT Token:", jwt_token)

        # Call the superclass method to handle the usual post processing
        return super().post(request, *args, **kwargs)
    '''
class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]  # Change to JWTAuthentication if you use JWT
    # authentication_classes = [JWTAuthentication] 

class UserDetailByIdAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer

class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer



# Travel Plan APIs

class TravelPlanCreateAPIView(generics.CreateAPIView):
    queryset = TravelPlan.objects.all()
    serializer_class = TravelPlanSerializer

class TravelPlanAPIView(generics.ListAPIView):
    queryset = TravelPlan.objects.all()
    serializer_class = TravelPlanSerializer

class TravelPlanDetailByIdAPIView(generics.RetrieveAPIView):
    queryset = TravelPlan.objects.all()
    lookup_field = 'id'
    serializer_class = TravelPlanSerializer

class TravelPlanUpdateAPIView(generics.UpdateAPIView):
    queryset = TravelPlan.objects.all()
    lookup_field = 'id'
    serializer_class = TravelPlanSerializer

class TravelPlanDeleteAPIView(generics.DestroyAPIView):
    queryset = TravelPlan.objects.all()
    lookup_field = 'id'
    serializer_class = TravelPlanSerializer



# Booking Plan APIs

class BookingsCreateAPIView(generics.CreateAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer

class BookingsAPIView(generics.ListAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer

class BookingsDetailByIdAPIView(generics.RetrieveAPIView):
    queryset = Bookings.objects.all()
    lookup_field = 'id'
    serializer_class = BookingsSerializer

class BookingsUpdateAPIView(generics.UpdateAPIView):
    queryset = Bookings.objects.all()
    lookup_field = 'id'
    serializer_class = BookingsSerializer

class BookingsDeleteAPIView(generics.DestroyAPIView):
    queryset = Bookings.objects.all()
    lookup_field = 'id'
    serializer_class = BookingsSerializer

# User helper API

class BookingsDetailByUserIdAPIView(generics.ListAPIView):
    # queryset = Bookings.objects.filter(user_id=id')
    # queryset = Bookings.objects.all()
    serializer_class = BookingsDetailsSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']  # Get the user ID from URL kwargs
        return Bookings.objects.filter(user_id=user_id)
        # return Bookings.objects.select_related('travel_plan_id').filter(user_id=user_id)