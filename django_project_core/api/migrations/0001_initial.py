# Generated by Django 5.1.1 on 2024-09-28 22:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField(blank=True, null=True)),
                ('ratings_count', models.IntegerField(blank=True, default=0, null=True)),
                ('average_rating', models.FloatField(blank=True, default=0.0, null=True)),
                ('text_reviews_count', models.IntegerField(blank=True, default=0, null=True)),
                ('work_ids', models.JSONField(blank=True, default=list, null=True)),
                ('book_ids', models.JSONField(blank=True, default=list, null=True)),
                ('works_count', models.IntegerField(blank=True, default=0, null=True)),
                ('external_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('fans_count', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('published_date', models.DateField(blank=True, null=True)),
                ('isbn', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('isbn13', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('asin', models.CharField(blank=True, max_length=10, null=True)),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('average_rating', models.FloatField(blank=True, default=0.0, null=True)),
                ('rating_dist', models.CharField(blank=True, max_length=255, null=True)),
                ('ratings_count', models.IntegerField(blank=True, default=0, null=True)),
                ('text_reviews_count', models.IntegerField(blank=True, default=0, null=True)),
                ('publication_date', models.CharField(blank=True, max_length=50, null=True)),
                ('original_publication_date', models.DateField(blank=True, null=True)),
                ('format', models.CharField(blank=True, max_length=50, null=True)),
                ('edition_information', models.CharField(blank=True, max_length=255, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('publisher', models.CharField(blank=True, max_length=255, null=True)),
                ('num_pages', models.IntegerField(blank=True, default=0, null=True)),
                ('series_id', models.CharField(blank=True, max_length=255, null=True)),
                ('series_name', models.CharField(blank=True, max_length=255, null=True)),
                ('series_position', models.CharField(blank=True, max_length=50, null=True)),
                ('is_favourite', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.author')),
            ],
        ),
        migrations.CreateModel(
            name='FavouriteBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'book')},
            },
        ),
    ]
