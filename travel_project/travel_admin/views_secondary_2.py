


from rest_framework import generics, views
from .models import User, TravelPlan, Bookings
from .serializers import UserSerializer, TravelPlanSerializer, BookingsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# This parameter will be added to each view that requires JWT authentication


class WelcomeView(views.APIView):
    def get(self, request):
        return Response({"message": "Welcome to the user API"}, status=status.HTTP_200_OK)

class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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


