import os
import csv
from django.core.management.base import BaseCommand
from django.db.models import Model
from reviews.models import Title, Category, Genre, TitleGenre, Review, Comment
from users.models import User


class Command(BaseCommand):
    help = 'Импорт данных в базу данных из файла csv'

    CHOISE_MODEL = {
        'titles': Title,
        'genre': Genre,
        'genre_title': TitleGenre,
        'category': Category(),
        'review': Review,
        'comments': Comment,
        'users': User,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path',
            type=str,
            help='The path to the dir with CSV files or to CSV file'
        )

    def get_csv_files(self, path: str) -> list:
        csv_files = []
        if os.path.isfile(path):
            if os.path.splitext(path)[-1] == '.csv':
                csv_files.append(path)
        else:
            for file in os.listdir(path):
                if os.path.splitext(file)[-1] == '.csv':
                    csv_files.append(os.path.join(path, file))
        return csv_files

    def get_model(self, file: str) -> Model:
        name = os.path.split(file)[-1].split('.')[0].lower()
        return self.CHOISE_MODEL.get(name)

    def handle(self, *args, **options):
        csv_files = self.get_csv_files(options['csv_path'])
        for file in csv_files:
            model = self.get_model(file)
            with open(file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    for column, value in row.items():
                        setattr(model, column, value)
                    model.save()
