from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (ReviewSerializer, CommentSerializer,
                          TitleSerializers, TitleGetSerializers,
                          GenreSerializers, CategorySerializers)
from reviews.models import Title, Review, Genre, Category
from .viewsets import ListCreateDeleteViewSet
from .filters import TitleFilters


class ReviewViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)
    serializer_class = ReviewSerializer
    # permission_classes = None # Add class

    def get_title(self) -> Title:
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)
    serializer_class = CommentSerializer
    # permission_classes = None #  Add class

    def get_review(self) -> Review:
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__pk=self.kwargs.get('title_id'),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete',)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializers
        return TitleSerializers


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    filter_backends = (SearchFilter,)
    search_fields = ('$name',)


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    filter_backends = (SearchFilter,)
    search_fields = ('$name',)
