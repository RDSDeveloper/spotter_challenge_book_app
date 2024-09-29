import sys
import os
import json
import django
from django.db import transaction

# Print the current working directory for debugging
print("Current working directory:", os.getcwd())

# Adjust the Python path
sys.path.append("/app")
sys.path.append("/app/django_project_core")
sys.path.append("/app/api")

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_core.settings")
django.setup()

from api.models import Author, Book

# Load and print the first item from authors.json
try:
    with open("/app/django_project_core/data/authors.json") as f:
        for line in f:
            first_author = json.loads(line)
            print("First author data:", first_author)
            break
except Exception as e:
    print(f"Error loading authors.json: {e}")

# Load and print the first item from books_partial.json
try:
    with open("/app/django_project_core/data/books_partial.json") as f:
        for line in f:
            first_book = json.loads(line)
            print("First book data:", first_book)
            break
except Exception as e:
    print(f"Error loading books_partial.json: {e}")

# Populate Author model
try:
    with transaction.atomic():
        author = Author.objects.create(
            name=first_author.get("name"),
            bio=first_author.get("about", ""),
            ratings_count=first_author.get("ratings_count", 0),
            average_rating=first_author.get("average_rating", 0.0),
            text_reviews_count=first_author.get("text_reviews_count", 0),
            work_ids=first_author.get("work_ids", []),
            book_ids=first_author.get("book_ids", []),
            works_count=first_author.get("works_count", 0),
            external_id=first_author.get("id"),
            gender=first_author.get("gender", ""),
            image_url=first_author.get("image_url", ""),
            fans_count=first_author.get("fans_count", 0),
        )
        print(f"Author created: {author.name}")
except Exception as e:
    print(f"Error creating author: {e}")

# Populate Book model
try:
    with transaction.atomic():
        author, created = Author.objects.get_or_create(
            external_id=first_book.get("author_id"),
            defaults={"name": first_book.get("author_name")},
        )

        book = Book.objects.create(
            title=first_book.get("title"),
            author=author,
            published_date=first_book.get("original_publication_date"),
            isbn=first_book.get("isbn", ""),
            isbn13=first_book.get("isbn13", ""),
            asin=first_book.get("asin", ""),
            language=first_book.get("language", ""),
            average_rating=first_book.get("average_rating", 0.0),
            rating_dist=first_book.get("rating_dist", ""),
            ratings_count=first_book.get("ratings_count", 0),
            text_reviews_count=first_book.get("text_reviews_count", 0),
            publication_date=first_book.get("publication_date", ""),
            format=first_book.get("format", ""),
            edition_information=first_book.get("edition_information", ""),
            image_url=first_book.get("image_url", ""),
            publisher=first_book.get("publisher", ""),
            num_pages=first_book.get("num_pages", 0),
            series_id=first_book.get("series_id", ""),
            series_name=first_book.get("series_name", ""),
            series_position=first_book.get("series_position", ""),
            description=first_book.get("description", ""), 
        )
        print(f"Book created: {book.title}")
except Exception as e:
    print(f"Error creating book: {e}")
