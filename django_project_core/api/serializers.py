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
    book = serializers.SerializerMethodField()

    class Meta:
        model = FavouriteBook
        fields = ["book"]

    def get_book(self, obj):
        return {
            "id": obj.book.id,
            "title": obj.book.title,
            "author": obj.book.author.name
        }

class AddToFavoritesSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

class RemoveFromFavoritesSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

class RecommendedBookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = ["title", "author"]