from django.contrib import admin
from .models import Title, Genre, Category, Review, Comment, TitleGenre


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'slug'
    )


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(TitleGenre)
