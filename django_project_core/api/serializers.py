from rest_framework import serializers
from .models import Author, Book, FavouriteBook


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class FavouriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteBook
        fields = "__all__"


class AddToFavoritesSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

class RemoveFromFavoritesSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
