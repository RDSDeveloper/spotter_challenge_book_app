from rest_framework import viewsets
from .models import Author, Book, FavouriteBook
from .serializers import AuthorSerializer, BookSerializer, FavouriteBookSerializer
from .mixins import CustomPermissionsMixin

class AuthorViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class FavouriteBookViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = FavouriteBook.objects.all()
    serializer_class = FavouriteBookSerializer