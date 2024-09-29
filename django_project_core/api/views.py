from rest_framework import viewsets, status, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book, FavouriteBook
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    FavouriteBookSerializer,
    AddToFavoritesSerializer,
    RemoveFromFavoritesSerializer,
)
from .mixins import CustomPermissionsMixin


class AuthorViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]


class BookViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "author__name"]


class FavouriteBookViewSet(CustomPermissionsMixin, viewsets.ModelViewSet):
    queryset = FavouriteBook.objects.all()
    serializer_class = FavouriteBookSerializer


class AddToFavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddToFavoritesSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user

            # Check if the user already has 20 favorite books
            if FavouriteBook.objects.filter(user=user).count() >= 20:
                return Response(
                    {
                        "error": "You can only have up to 20 favorite books. Please remove some before adding new ones."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            book_id = serializer.validated_data.get("book_id")
            try:
                book = Book.objects.get(id=book_id)
                FavouriteBook.objects.create(user=user, book=book)

                # Get recommendations
                recommendations = self.get_recommendations(user)

                return Response(
                    {
                        "status": "book added to favorites",
                        "recommendations": recommendations,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Book.DoesNotExist:
                return Response(
                    {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_recommendations(self, user):
        favorite_books = FavouriteBook.objects.filter(user=user).values_list(
            "book", flat=True
        )
        favorite_books = Book.objects.filter(id__in=favorite_books)

        if not favorite_books.exists():
            return []

        # Combine all descriptions of favorite books
        favorite_books_descriptions = " ".join(
            [book.description for book in favorite_books if book.description]
        )

        # Get all books excluding the user's favorite books
        other_books = Book.objects.exclude(id__in=favorite_books)

        if not other_books.exists():
            return []

        # Combine all descriptions of other books
        other_books_descriptions = [
            book.description for book in other_books if book.description
        ]

        # Use TF-IDF Vectorizer to convert text to vectors
        vectorizer = TfidfVectorizer().fit_transform(
            [favorite_books_descriptions] + other_books_descriptions
        )
        vectors = vectorizer.toarray()

        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

        # Get top 5 similar books
        similar_books_indices = cosine_similarities.argsort()[-5:][::-1]
        similar_books = [other_books[i] for i in similar_books_indices]

        return BookSerializer(similar_books, many=True).data


class RemoveFromFavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RemoveFromFavoritesSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            book_id = serializer.validated_data.get("book_id")
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
                    {"error": "Favorite book not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListFavoriteBooksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        favourite_books = FavouriteBook.objects.filter(user=user)
        serializer = FavouriteBookSerializer(favourite_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
