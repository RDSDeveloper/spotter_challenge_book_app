from rest_framework import viewsets
from .models import Author, Book, FavouriteBook
from .serializers import AuthorSerializer, BookSerializer, FavouriteBookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class FavouriteBookViewSet(viewsets.ModelViewSet):
    queryset = FavouriteBook.objects.all()
    serializer_class = FavouriteBookSerializer