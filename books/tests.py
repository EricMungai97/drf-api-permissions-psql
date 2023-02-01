from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Book


class BookTests(APITestCase):
    # In Python, the @classmethod decorator is used to declare a method in the class as a class method that can be called using ClassName.MethodName()
    # click the blue circle, this overrides a particular method
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_book = Book.objects.create(
            Title="rake",
            owner=testuser1,
            description="Better for collecting leaves than a shovel.",
            Author='munga',
        )
        test_book.save()

    # NEW
    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_books_model(self):
        book = Book.objects.get(id=1)
        actual_owner = str(book.owner)
        actual_title = str(book.Title)
        actual_description = str(book.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_title, "rake")
        self.assertEqual(
            actual_description, "Better for collecting leaves than a shovel."
        )

    def test_get_book_list(self):
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = response.data
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["Title"], "rake")

    def test_get_book_by_id(self):
        url = reverse("book_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = response.data
        self.assertEqual(book["Title"], "rake")

    def test_create_book(self):
        url = reverse("book_list")
        data = {"owner": 1, "Title": "spoon", "Author": "munga", "description": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        books = Book.objects.all()
        self.assertEqual(len(books), 2)
        self.assertEqual(Book.objects.get(id=2).Title, "spoon")

    def test_update_book(self):
        url = reverse("book_detail", args=(1,))
        data = {
            "owner": 1,
            "Title": "rake",
            "Author": "munga",
            "description": "pole with a crossbar toothed like a comb."
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id=1)
        self.assertEqual(book.Title, data["Title"])
        self.assertEqual(book.owner.id, data["owner"])
        self.assertEqual(book.description, data["description"])
        self.assertEqual(book.Author, data["Author"])

    def test_delete_book(self):
        url = reverse("book_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        books = Book.objects.all()
        self.assertEqual(len(books), 0)

    # New
    def test_authentication_required(self):
        self.client.logout()
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
