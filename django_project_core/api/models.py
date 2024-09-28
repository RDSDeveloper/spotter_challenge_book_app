from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    ratings_count = models.IntegerField(default=0, blank=True, null=True)
    average_rating = models.FloatField(default=0.0, blank=True, null=True)
    text_reviews_count = models.IntegerField(default=0, blank=True, null=True)
    work_ids = models.JSONField(default=list, blank=True, null=True)
    book_ids = models.JSONField(default=list, blank=True, null=True)
    works_count = models.IntegerField(default=0, blank=True, null=True)
    external_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    fans_count = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    isbn13 = models.CharField(max_length=13, unique=True, blank=True, null=True)
    asin = models.CharField(max_length=10, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    average_rating = models.FloatField(default=0.0, blank=True, null=True)
    rating_dist = models.CharField(max_length=255, blank=True, null=True)
    ratings_count = models.IntegerField(default=0, blank=True, null=True)
    text_reviews_count = models.IntegerField(default=0, blank=True, null=True)
    publication_date = models.CharField(max_length=50, blank=True, null=True)
    original_publication_date = models.DateField(blank=True, null=True)
    format = models.CharField(max_length=50, blank=True, null=True)
    edition_information = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    num_pages = models.IntegerField(default=0, blank=True, null=True)
    series_id = models.CharField(max_length=255, blank=True, null=True)
    series_name = models.CharField(max_length=255, blank=True, null=True)
    series_position = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title


class FavouriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
