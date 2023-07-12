from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (ReviewSerializer, CommentSerializer,
                          TitleSerializers, TitleGetSerializers,
                          GenreSerializers, CategorySerializers,
                          UserSerializer, IssueTokenSerializer)
from reviews.models import Title, Review, Genre, Category, User
from .viewsets import ListCreateDeleteViewSet, CreateViewSet
from .filters import TitleFilters
from .permissions import (IsAuthorModeratorAdminOrReadOnly, IsAdminOrReadOnly)


class SignUpUserViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Conformation code',
            message=confirmation_code,
            from_email=settings.NOREPLY_EMAIL,
            recipient_list=(user.email, ),
        )


class IssueTokenAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = IssueTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username')
            )
            if default_token_generator.check_token(
                user, serializer.validated_data.get('confirmation_code')
            ):
                return Response(
                    data={'token': f'{RefreshToken.for_user(user).access_token}'},
                    status=status.HTTP_200_OK,
                )
            return Response(
                data={'token': 'Указан некорректный код подтверждения.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

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
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

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
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializers
        return TitleSerializers


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    filter_backends = (SearchFilter,)
    search_fields = ('$name',)
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    filter_backends = (SearchFilter,)
    search_fields = ('$name',)
    permission_classes = (IsAdminOrReadOnly,)
