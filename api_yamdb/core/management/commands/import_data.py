from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Импорт данных в базу данных из файла csv'

    def handle(self, *args, **kwargs):
        pass
