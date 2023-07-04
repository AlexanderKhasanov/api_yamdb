from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    pass


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
    score = models.IntegerField(
        verbose_name='Рейтинг произведения',
        choices=[(i, i) for i in range(1, 11)],
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
