from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Title, Genre, Category, Review, Comment, TitleGenre


User = get_user_model()


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'slug'
    )


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'slug'
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username'
    )


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description', 'category'
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(TitleGenre)
