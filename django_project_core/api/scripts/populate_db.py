import json
import os
import django
from django_project_core.api.models import Author, Book

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_core.settings")
django.setup()

# Load JSON data
with open("data/authors.json") as f:
    authors_data = json.load(f)

with open("data/books.json") as f:
    books_data = json.load(f)

# Populate Author model
for author_data in authors_data["root"]:
    Author.objects.create(
        name=author_data.get("name"),
        bio=author_data.get("about", ""),
        ratings_count=author_data.get("ratings_count", 0),
        average_rating=author_data.get("average_rating", 0.0),
        text_reviews_count=author_data.get("text_reviews_count", 0),
        work_ids=author_data.get("work_ids", []),
        book_ids=author_data.get("book_ids", []),
        works_count=author_data.get("works_count", 0),
        external_id=author_data.get("id"),
        gender=author_data.get("gender", ""),
        image_url=author_data.get("image_url", ""),
        fans_count=author_data.get("fans_count", 0),
    )

# Populate Book model
for book_data in books_data["root"]:
    author, created = Author.objects.get_or_create(
        external_id=book_data.get("author_id"),
        defaults={"name": book_data.get("author_name")},
    )

    Book.objects.create(
        title=book_data.get("title"),
        author=author,
        published_date=book_data.get("original_publication_date"),
        isbn=book_data.get("isbn", ""),
        isbn13=book_data.get("isbn13", ""),
        asin=book_data.get("asin", ""),
        language=book_data.get("language", ""),
        average_rating=book_data.get("average_rating", 0.0),
        rating_dist=book_data.get("rating_dist", ""),
        ratings_count=book_data.get("ratings_count", 0),
        text_reviews_count=book_data.get("text_reviews_count", 0),
        publication_date=book_data.get("publication_date", ""),
        format=book_data.get("format", ""),
        edition_information=book_data.get("edition_information", ""),
        image_url=book_data.get("image_url", ""),
        publisher=book_data.get("publisher", ""),
        num_pages=book_data.get("num_pages", 0),
        series_id=book_data.get("series_id", ""),
        series_name=book_data.get("series_name", ""),
        series_position=book_data.get("series_position", ""),
        is_favourite=False,
    )
