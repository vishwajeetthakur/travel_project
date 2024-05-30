from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from travel_admin.models import User, TravelPlan, Bookings
from rest_framework_simplejwt.tokens import RefreshToken


class APITests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='admin@example.com', name='Admin User', password='adminpassword')
        self.user = User.objects.create_user(email='user@example.com', name='Test User', password='testpassword')
        self.travel_plan = TravelPlan.objects.create(destination='Test Destination', cost=100, description='Test Description')
        self.booking = Bookings.objects.create(user_id=self.user, travel_plan_id=self.travel_plan)
        self.client.force_authenticate(user=self.user)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_user_registration(self):
        url = reverse('User-register')
        data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'newpassword',
            'password2': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_user_login(self):
        url = reverse('user_and_admin_login')
        data = {
            'email': self.user.email,
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_profile(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['name'], self.user.name)

    def test_change_password(self):
        url = reverse('change-password')
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword',
            'confirm_new_password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Password changed successfully')

    def test_logout(self):
        url = reverse('user_and_admin_logout')
        tokens = self.get_tokens_for_user(self.user)
        data = {
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logged out successfully')

    def test_admin_see_all_users(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('Admin-see-all-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_booking_details(self):
        url = reverse('User-Bookings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_booking(self):
        url = reverse('User-Plan-Booking', args=[self.travel_plan.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    '''
    def test_edit_booking(self):
        url = reverse('User-Bookings', args=[self.booking.id])
        data = {
            'travel_plan_id': self.travel_plan.id,
            'user_id': self.user.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    '''
    
    def test_delete_booking(self):
        url = reverse('User-Bookings', args=[self.booking.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_travel_plan(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('Admin-Plan-Creation')
        data = {
            'destination': 'New Destination',
            'cost': 200,
            'description': 'New Description'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_travel_plan(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('Admin-Plan-Edit', args=[self.travel_plan.id])
        data = {
            'destination': 'Updated Destination',
            'cost': 300,
            'description': 'Updated Description'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_travel_plan(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('Admin-Plan-Delete', args=[self.travel_plan.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_all_travel_plans(self):
        url = reverse('User_and_Admin_both-Plan-View')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_details_with_bookings(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('Admin-users-details with-Bookings-View')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_booking_details_with_travel_plan(self):
        url = reverse('User-Bookings-View')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Run the tests with the following command:
# python manage.py test travel_admin
