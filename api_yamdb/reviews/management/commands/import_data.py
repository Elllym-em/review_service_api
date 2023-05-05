import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

MODELS_DATA = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

CSV_PATH = f'{settings.BASE_DIR}/static/data/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model, csv_f in MODELS_DATA.items():
            with open(
                str(CSV_PATH) + csv_f, 'r', newline=''
            ) as file:
                reader = csv.DictReader(file)
                records = []
                for row in reader:
                    records.append(model(**row))
            model.objects.bulk_create(records)

        with open(
            str(CSV_PATH) + 'genre_title.csv', 'r', newline=''
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                title.genre.add(row['genre_id'])

        self.stdout.write(self.style.SUCCESS(
            'Данные успешно загружены.'
        ))
