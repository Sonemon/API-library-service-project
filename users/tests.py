from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@test.com",
            "password": "testpass123",
        }
        self.user = User.objects.create_user(**self.user_data)

    # Registration tests
    def test_user_registration(self):
        url = reverse("users:create")
        data = {
            "email": "newuser@test.com",
            "password": "newpassword123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_user_registration_short_password(self):
        url = reverse("users:create")
        data = {
            "email": "newuser@test.com",
            "password": "123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_email(self):
        url = reverse("users:create")
        data = {
            "email": "invalidemail",
            "password": "validpassword123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        url = reverse("users:create")
        data = {
            "email": self.user_data["email"],
            "password": "newpassword123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Token tests
    def test_token_obtain(self):
        url = reverse("users:token_obtain_pair")
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_invalid_credentials(self):
        url = reverse("users:token_obtain_pair")
        data = {
            "email": self.user_data["email"],
            "password": "wrongpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        # First get refresh token
        token_url = reverse("users:token_obtain_pair")
        token_response = self.client.post(token_url, self.user_data)
        refresh_token = token_response.data["refresh"]

        # Then refresh it
        refresh_url = reverse("users:token_refresh")
        response = self.client.post(refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # Manage user tests
    def test_manage_user_unauthorized(self):
        url = reverse("users:manage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_manage_user_authorized(self):
        # Get token first
        token_url = reverse("users:token_obtain_pair")
        token_response = self.client.post(token_url, self.user_data)
        access_token = token_response.data["access"]

        # Test authorized access
        url = reverse("users:manage")
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {access_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_manage_user_update(self):
        # Get token first
        token_url = reverse("users:token_obtain_pair")
        token_response = self.client.post(token_url, self.user_data)
        access_token = token_response.data["access"]

        # Test update
        url = reverse("users:manage")
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {access_token}")
        update_data = {"password": "newpass123"}
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify password changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass123"))
