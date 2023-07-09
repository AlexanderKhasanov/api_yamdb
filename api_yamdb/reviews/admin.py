from django.contrib import admin
from .models import Title, Genre, Category, Review, Comment, TitleGenre


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(TitleGenre)
