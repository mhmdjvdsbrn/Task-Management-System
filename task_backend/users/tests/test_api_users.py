from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from task_backend.users.models import BaseUser, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterApiTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:register')  # Correcting the URL name here
        self.valid_payload = {
            "phone": "09123456789",
            "password": "StrongP@ssword1",
            "confirm_password": "StrongP@ssword1"
        }

    def test_register_valid(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().phone, self.valid_payload['phone'])

    def test_register_phone_already_exists(self):
        User.objects.create_user(phone="09123456789", password="StrongP@ssword1")
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Phone number already taken", response.data['phone'][0])

    def test_register_password_mismatch(self):
        self.valid_payload['confirm_password'] = "DifferentP@ssword2"
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Confirm password does not match password", response.data['non_field_errors'][0])


class CompleteProfileApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone="09123456789", password="StrongP@ssword1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('users:profile_verify')  # Correcting the URL name here
        self.valid_payload = {
            "first_name": "javad",
            "last_name": "sbrn",
            "gender": Profile.MALE,
        }

    def test_complete_profile_valid(self):
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.first_name, "javad")
        self.assertEqual(profile.last_name, "sbrn")
        self.assertEqual(profile.gender, Profile.MALE)

    def test_complete_profile_missing_fields(self):
        invalid_payload = {
            "first_name": "javad",
            # Missing  last_name, and gender
        }
        response = self.client.put(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data['last_name'][0])
        self.assertIn("This field is required.", response.data['gender'][0])



class ViewProfileApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone="09123456789", password="StrongP@ssword1")
        self.profile = Profile.objects.create(
            user=self.user, first_name="javad", last_name="sbrn", gender=Profile.MALE
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('users:profile')  # Correcting the URL name here

    def test_view_profile_valid(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.profile.first_name)
        self.assertEqual(response.data['last_name'], self.profile.last_name)
        self.assertEqual(response.data['gender'], self.profile.gender)

    def test_view_profile_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
