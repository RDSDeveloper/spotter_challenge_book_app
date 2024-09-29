from rest_framework import viewsets, status, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book, FavouriteBook
from .serializers import AuthorSerializer, BookSerializer, FavouriteBookSerializer
from .mixins import CustomPermissionsMixin

class AuthorViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

class BookViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'author__name']

class FavouriteBookViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = FavouriteBook.objects.all()
    serializer_class = FavouriteBookSerializer

class AddToFavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        book_id = request.data.get("book_id")
        try:
            book = Book.objects.get(id=book_id)
            FavouriteBook.objects.create(user=user, book=book)
            return Response(
                {"status": "book added to favorites"}, status=status.HTTP_201_CREATED
            )
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromFavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        book_id = request.data.get("book_id")
        try:
            book = Book.objects.get(id=book_id)
            favourite_book = FavouriteBook.objects.get(user=user, book=book)
            favourite_book.delete()
            return Response(
                {"status": "book removed from favorites"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FavouriteBook.DoesNotExist:
            return Response(
                {"error": "Favorite book not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)