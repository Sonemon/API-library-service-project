from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class BookUnauthorizedTests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=5.00,
        )

    def test_get_books_list(self):
        url = reverse("books:books-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book_unauthorized(self):
        url = reverse("books:books-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 3.50,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_unauthorized(self):
        url = reverse("books:books-detail", args=[self.book.id])
        data = {"title": "Updated Book"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookUserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=5.00,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_book_forbidden(self):
        url = reverse("books:books-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 3.50,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_forbidden(self):
        url = reverse("books:books-detail", args=[self.book.id])
        data = {"title": "Updated Book"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookAdminTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="adminpass",
            is_staff=True
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=5.00,
        )
        self.client.force_authenticate(user=self.admin)

    def test_create_book(self):
        url = reverse("books:books-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 3.50,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=response.data["id"]).title, "New Book")

    def test_create_book_with_invalid_data(self):
        url = reverse("books:books-list")
        data = {
            "title": "",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": -5,
            "daily_fee": -3.50,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 1)

    def test_unique_constraint(self):
        url = reverse("books:books-list")
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 5.00,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_update_book(self):
        url = reverse("books:books-detail", args=[self.book.id])
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "cover": "SOFT",
            "inventory": 15,
            "daily_fee": 4.00,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        url = reverse("books:books-detail", args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
