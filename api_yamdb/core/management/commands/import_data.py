import os
import csv
from django.core.management.base import BaseCommand
from django.db import utils
from django.core import exceptions
from django.contrib.auth import get_user_model
from reviews.models import Title, Category, Genre, TitleGenre, Review, Comment

User = get_user_model()


class Command(BaseCommand):
    help = ('Импорт данных в базу данных из файла csv. '
            'Все имеющиеся в базе данные будут удалены')

    RELATED_MODELS = {
        'title': Title,
        'genre': Genre,
        'category': Category,
        'review': Review,
        'author': User,
    }
    FILE_TABLE = [
        ('category.csv', Category),
        ('genre.csv', Genre),
        ('users.csv', User),
        ('titles.csv', Title),
        ('genre_title.csv', TitleGenre),
        ('review.csv', Review),
        ('comments.csv', Comment),
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path', type=str,
            help='The path to the dir with CSV files or to CSV file'
        )

    def rename_column(self, fieldnames: list) -> list:
        new_fieldnames = []
        for field in fieldnames:
            start_id = field.find('_id')
            if start_id != -1:
                field = field[:start_id]
            new_fieldnames.append(field)
        return new_fieldnames

    def create_data(self, reader, model):
        for row in reader:
            for column, value in row.items():
                foreign_key = self.RELATED_MODELS.get(column)
                if foreign_key is not None:
                    row[column] = foreign_key.objects.get(pk=value)
            model.objects.get_or_create(**row)

    def handle(self, *args, **options):
        try:
            csv_dir = options['csv_path']
            for file, model in self.FILE_TABLE:
                with open(os.path.join(csv_dir, file), 'r',
                          encoding='utf-8', errors='ignore') as csv_file:
                    reader = csv.DictReader(csv_file)
                    reader.fieldnames = self.rename_column(reader.fieldnames)
                    model.objects.all().delete()
                    self.create_data(reader, model)
        except FileNotFoundError:
            print(f'Ошибка! Указанная папка должна содержать файл {file}')
        except utils.IntegrityError as error:
            print(f'Ошибка при импорте данных из файла {file}: {error}')
        except exceptions.FieldError as error:
            print(f'Ошибка при импорте данных из файла {file}: {error}')
            print('Столбцы в файле должны быть названы как в модели')
        except Exception as error:
            print(f'Ошибка при импорте данных из файла {file}: {error}')
        else:
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
