from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.constraints import UniqueConstraint
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    RegexValidator)


USER_ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=16,
        choices=USER_ROLE,
        default='user'
    )
    email = models.EmailField(
        verbose_name='e-mail адрес',
        max_length=254,
        unique=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['pk']

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Укажите название категории (не более 256 символов)'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное имя категории',
        help_text='Укажите уникальное имя категории (не более 50 символов)',
        validators=[
            RegexValidator(
                r'^[-a-zA-Z0-9_]+$',
                'Для поля можно использовать символы: a-z A-Z 0-9 _ -'
            )
        ]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['pk']

    def __str__(self) -> str:
        return self.name[:30]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Укажите название жанра (не более 256 символов)'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное имя жанра',
        help_text='Укажите уникальное имя жанра (не более 50 символов)',
        validators=[
            RegexValidator(
                r'^[-a-zA-Z0-9_]+$',
                'Для поля можно использовать символы: a-z A-Z 0-9 _ -'
            )
        ]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['pk']

    def __str__(self) -> str:
        return self.name[:30]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        help_text='Введите название произведения (не более 256 символов)'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text='Укажите год выпуска произведения'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения',
        help_text='Укажите описание произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория произведения',
        help_text='Укажите, к какой категории относится произведение'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='genres',
        verbose_name='Жанры произведения',
        help_text='Укажите, к какому жанру относится произведение'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['pk']

    def __str__(self) -> str:
        return self.name[:30]


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('title', 'genre')
        ordering = ['pk']

    def __str__(self) -> str:
        return f'{self.title}: {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveIntegerField(
        verbose_name='Рейтинг произведения',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [UniqueConstraint(
            fields=['title', 'author'],
            name='unique_title_for_author_review'
        )]

    def __str__(self) -> str:
        return self.text[:30]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.CharField(
        verbose_name='Текст комментария',
        max_length=155,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text[:30]
