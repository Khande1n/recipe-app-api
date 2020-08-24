from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('token:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_valid_successful(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@nikhil.com',
            'password': 'nikhil123',
            'name': 'Nikhil Khandelwal'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test that users already exists"""
        payload = {
            'email': 'nikhil@nikhil.com',
            'password': 'nikhil123',
            'name': 'nikhil khandelwal'
        }
        user = create_user(**payload)
        
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password should be more than 5 characters"""
        payload = {
            'email': 'nikhil@nikhil.com',
            'password': 'pw',
            'name': 'nikhil khandelwal'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for a user"""
        payload = {
            'email': 'nikhil@nikhil.com',
            'password': 'nikhil123',
            'name': 'Nikhil Khandelwal'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        create_user(email='nikhil@nikhil.com', password='nikhil123')
        payload = {
            'email': 'nikhil@nikhil.com',
            'password': 'wrongpass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does'nt exists"""
        payload = {
            'email': 'nikhil@nikhil.com',
            'password': 'wrongpass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that token creation require email and password fields"""
        res = self.client.post(TOKEN_URL, {email: 'one', password: ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)