from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    TitleSerializers,
    TitleGetSerializers,
    GenreSerializers,
    CategorySerializers,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
)
from reviews.models import Title, Review, Genre, Category, User
from .viewsets import ListCreateDeleteViewSet
from .filters import TitleFilters
from .permissions import (
    IsAuthorModeratorAdminOrReadOnly,
    IsAdminOrReadOnly,
    IsAdmin,
    IsOwner,
)

User = get_user_model()


class SignUpUserViewSet(APIView):
    permission_classes = (AllowAny,)

    def send_confirmation_code(self, user):
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject="Conformation code",
            message=confirmation_code,
            from_email=settings.NOREPLY_EMAIL,
            recipient_list=(user.email,),
        )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        user = User.objects.filter(
            username=request.data.get("username"),
            email=request.data.get("email")
        )
        if user.exists():
            self.send_confirmation_code(user.first())
            return Response(serializer.initial_data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.validated_data.get("username"),
                email=serializer.validated_data.get("email"),
            )
            self.send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data.get("username")
            )
            if default_token_generator.check_token(
                user, serializer.validated_data.get("confirmation_code")
            ):
                return Response(
                    {"token": f"{RefreshToken.for_user(user).access_token}"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"token": "Указан некорректный код подтверждения."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSet):
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_title(self) -> Title:
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        user = self.request.user
        if Review.objects.filter(title=title, author=user).exists():
            raise ValidationError(
                "На одно произведение можно оставить только один отзыв"
            )
        serializer.save(
            author=user,
            title=title,
        )


class CommentViewSet(ModelViewSet):
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_review(self) -> Review:
        return get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            title__pk=self.kwargs.get("title_id"),
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
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleGetSerializers
        return TitleSerializers


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    filter_backends = (SearchFilter,)
    search_fields = ("$name",)
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    filter_backends = (SearchFilter,)
    search_fields = ("$name",)
    permission_classes = (IsAdminOrReadOnly,)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("$username",)
    permission_classes = (IsAdmin,)
    lookup_field = "username"
    lookup_value_regex = r"[\w.@+-]+"

    @action(
        detail=False,
        methods=("get", "patch"),
        url_path="me",
        permission_classes=(IsOwner,),
    )
    def user_profile(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            if "role" in serializer.validated_data.keys():
                serializer.validated_data.pop("role")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
