from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from reviews.models import Title, Genre, Category
from .serializers import TitleSerializers, TitleGetSerializers


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializers
        return TitleSerializers
"""
    def perform_create(self, serializer):
        genre_slug = serializer.validated_data.get('genre')
        print(genre_slug)
        category_slug = serializer.validated_data.get('category')
        genre = get_object_or_404(Genre, slug=genre_slug)
        category = get_object_or_404(Category, slug=category_slug)
        serializer.save(
            genre=genre,
            category=category
        )"""
