from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=16,
        choices=CHOICES,
        default='user'
    )
    email = models.EmailField(
        verbose_name='e-mail адрес',
        max_length=254
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'moderator' or self.is_superuser or self.is_staff
