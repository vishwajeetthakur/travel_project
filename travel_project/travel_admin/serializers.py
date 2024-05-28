# serializers.py
from rest_framework import serializers
from .models import User, TravelPlan, Bookings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        fields = ['id', 'email', 'name', 'password']

class TravelPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlan
        # fields = '__all__'
        fields = ['id', 'destination', 'cost', 'description']


class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['id', 'user_id', 'travel_plan_id']

class BookingsDetailsSerializer(serializers.ModelSerializer):
    # travel_plan = TravelPlanSerializer()  # Nested serializer for TravelPlan
    travel_plan = TravelPlanSerializer(source='travel_plan_id', read_only=True)

    class Meta:
        model = Bookings # user_id, travel_plan_id
        fields = ['id', 'user_id', 'travel_plan']



class UserDetailsWithBookingsSerializer(serializers.ModelSerializer):
    # travel_plan = TravelPlanSerializer()  # Nested serializer for TravelPlan
    # bookings = BookingsDetailsSerializer(source='user_id', read_only=True)
    # travel_plan = BookingsDetailsSerializer(source='user_id', read_only=True)
    
    # travel_plan = TravelPlanSerializer(source='travel_plan_id', read_only=True)
    bookings = BookingsSerializer(source='Bookings_set', read_only=True)

    class Meta:
        model = User # user_id, travel_plan_id
        fields = ['id', 'user_id', 'bookings']
        # fields = ['id', 'user_id', 'travel_plan']


'''
[
    {
        id: 1,
        name: vicky,
        email: vicky@gmail.com,
        password: sdfsf,
        bookings: [{
            booking_id: 1,
            travel_plan: {
                id: 1,
                descination: sdfsf,
                cost: sdfsfd,
                description: dfsdfdf
            },
            {
            booking_id: 2,
            travel_plan: {
                id: 2,
                descination: sdfsf,
                cost: sdfsfd,
                description: dfsdfdf
            }
          ]
        }
    }
]

'''

# Serilzer used for getting bookings for sinelge user
class BookingSerializer(serializers.ModelSerializer):
    travel_details = TravelPlanSerializer(source='travel_plan_id') # fields = ['id', 'destination', 'cost', 'description']

    class Meta:
        model = Bookings
        fields = ['id', 'travel_details',]



class UserSerializer2(serializers.ModelSerializer):
    bookings = BookingsDetailsSerializer(many=True, source='bookings_set') # 1: bookings_set[1,2]

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'bookings']


# 
class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'password2']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)
  

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']


class UserProfileBookingSerializer(serializers.ModelSerializer):
    travel_plan = TravelPlanSerializer(source='travel_plan_id')  # Nested serializer for the associated travel plan

    class Meta:
        model = Bookings
        fields = ('id', 'travel_plan')  # Include additional fields as needed

  #  class Meta:
  #   model = User
  #   fields = ['id', 'email', 'name']



# change password
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Check that the new password and confirm new password match.
        Also, ensure the old password and new password are not the same.
        """
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "New password and confirm new password do not match."})

        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})

        return data

    def validate_new_password(self, value):
        # Additional password validation can be added here if needed
        return value