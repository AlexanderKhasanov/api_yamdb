from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ReviewSerializer, CommentSerializer
from reviews.models import Title, Review


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = None # Add class
    pagination_class = LimitOffsetPagination

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
    serializer_class = CommentSerializer
    # permission_classes = None #  Add class
    pagination_class = LimitOffsetPagination

    def get_review(self) -> Review:
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_review(),
        )
