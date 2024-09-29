import sys
import os
import json
import django
from django.db import transaction, IntegrityError
from datetime import datetime

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

# Load and print the first 100 items from authors.json
authors = []
try:
    with open("/app/django_project_core/data/authors.json") as f:
        for i, line in enumerate(f):
            if i >= 100:
                break
            author_data = json.loads(line)
            authors.append(author_data)
            print(f"Author data {i+1}:", author_data)
except Exception as e:
    print(f"Error loading authors.json: {e}")

# Load and print the first 100 items from books_partial.json
books = []
try:
    with open("/app/django_project_core/data/books_partial.json") as f:
        for i, line in enumerate(f):
            if i >= 100:
                break
            book_data = json.loads(line)
            books.append(book_data)
            print(f"Book data {i+1}:", book_data)
except Exception as e:
    print(f"Error loading books_partial.json: {e}")


def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


# Populate Author model
try:
    with transaction.atomic():
        for author_data in authors:
            author, created = Author.objects.get_or_create(
                external_id=author_data.get("id"),
                defaults={
                    "name": author_data.get("name"),
                    "bio": author_data.get("about", ""),
                    "ratings_count": author_data.get("ratings_count", 0),
                    "average_rating": author_data.get("average_rating", 0.0),
                    "text_reviews_count": author_data.get("text_reviews_count", 0),
                    "work_ids": author_data.get("work_ids", []),
                    "book_ids": author_data.get("book_ids", []),
                    "works_count": author_data.get("works_count", 0),
                    "gender": author_data.get("gender", ""),
                    "image_url": author_data.get("image_url", ""),
                    "fans_count": author_data.get("fans_count", 0),
                },
            )
            if created:
                print(f"Author created: {author.name}")
            else:
                print(f"Author already exists: {author.name}")
except Exception as e:
    print(f"Error creating authors: {e}")

# Populate Book model
try:
    with transaction.atomic():
        for book_data in books:
            author, created = Author.objects.get_or_create(
                external_id=book_data.get("author_id"),
                defaults={"name": book_data.get("author_name")},
            )

            # Skip books with empty ISBN to avoid unique constraint violation
            if not book_data.get("isbn"):
                print(f"Skipping book '{book_data.get('title')}' due to empty ISBN")
                continue

            # Validate and format the published_date
            published_date = validate_date(book_data.get("original_publication_date"))
            if not published_date:
                print(
                    f"Skipping book '{book_data.get('title')}' due to invalid date format"
                )
                continue

            try:
                book, created = Book.objects.get_or_create(
                    title=book_data.get("title"),
                    author=author,
                    defaults={
                        "published_date": published_date,
                        "isbn": book_data.get("isbn", ""),
                        "isbn13": book_data.get("isbn13", ""),
                        "asin": book_data.get("asin", ""),
                        "language": book_data.get("language", ""),
                        "average_rating": book_data.get("average_rating", 0.0),
                        "rating_dist": book_data.get("rating_dist", ""),
                        "ratings_count": book_data.get("ratings_count", 0),
                        "text_reviews_count": book_data.get("text_reviews_count", 0),
                        "publication_date": book_data.get("publication_date", ""),
                        "format": book_data.get("format", ""),
                        "edition_information": book_data.get("edition_information", ""),
                        "image_url": book_data.get("image_url", ""),
                        "publisher": book_data.get("publisher", ""),
                        "num_pages": (
                            int(book_data.get("num_pages", 0))
                            if book_data.get("num_pages")
                            else 0
                        ),
                        "series_id": book_data.get("series_id", ""),
                        "series_name": book_data.get("series_name", ""),
                        "series_position": book_data.get("series_position", ""),
                        "description": book_data.get("description", ""),
                    },
                )
                if created:
                    print(f"Book created: {book.title}")
                else:
                    print(f"Book already exists: {book.title}")
            except IntegrityError as e:
                print(f"Error creating book '{book_data.get('title')}': {e}")
except Exception as e:
    print(f"Error creating books: {e}")
