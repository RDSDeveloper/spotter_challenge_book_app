from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import AuthorSerializer, BookSerializer, FavouriteBookSerializer
from .models import Author, Book, FavouriteBook


class AuthorViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.author = Author.objects.create(name="Test Author")

    def test_list_authors(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_author(self):
        data = {"name": "New Author"}
        response = self.client.post(reverse('author-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class BookViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", author=self.author)

    def test_list_books(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        data = {"title": "New Book", "author": self.author.id}
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthorSerializerTest(APITestCase):
    def test_author_serializer(self):
        author = Author.objects.create(name="Test Author")
        serializer = AuthorSerializer(author)
        self.assertEqual(serializer.data["name"], "Test Author")


class BookSerializerTest(APITestCase):
    def test_book_serializer(self):
        author = Author.objects.create(name="Test Author")
        book = Book.objects.create(title="Test Book", author=author)
        serializer = BookSerializer(book)
        self.assertEqual(serializer.data["title"], "Test Book")


class FavouriteBookSerializerTest(APITestCase):
    def test_favourite_book_serializer(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        author = Author.objects.create(name="Test Author")
        book = Book.objects.create(title="Test Book", author=author)
        favourite_book = FavouriteBook.objects.create(user=user, book=book)
        serializer = FavouriteBookSerializer(favourite_book)
        self.assertEqual(serializer.data["book"]["title"], "Test Book")


class AuthorModelTest(TestCase):
    def test_create_author(self):
        author = Author.objects.create(name="Test Author")
        self.assertEqual(author.name, "Test Author")


class BookModelTest(TestCase):
    def test_create_book(self):
        author = Author.objects.create(name="Test Author")
        book = Book.objects.create(title="Test Book", author=author)
        self.assertEqual(book.title, "Test Book")


class FavouriteBookModelTest(TestCase):
    def test_create_favourite_book(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        author = Author.objects.create(name="Test Author")
        book = Book.objects.create(title="Test Book", author=author)
        favourite_book = FavouriteBook.objects.create(user=user, book=book)
        self.assertEqual(favourite_book.book.title, "Test Book")


class AuthorSerializerTest(APITestCase):
    def test_author_serializer(self):
        author = Author.objects.create(name="Test Author")
        serializer = AuthorSerializer(author)
        self.assertEqual(serializer.data["name"], "Test Author")


class BookSerializerTest(APITestCase):
    def test_book_serializer(self):
        author = Author.objects.create(name="Test Author")
        book = Book.objects.create(title="Test Book", author=author)
        serializer = BookSerializer(book)
        self.assertEqual(serializer.data["title"], "Test Book")


class FavouriteBookSerializerTest(APITestCase):
    def test_favourite_book_serializer(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        author = Author.objects.create(name="Test Author")
        book = Book.objects.create(title="Test Book", author=author)
        favourite_book = FavouriteBook.objects.create(user=user, book=book)
        serializer = FavouriteBookSerializer(favourite_book)
        self.assertEqual(serializer.data["book"]["title"], "Test Book")
