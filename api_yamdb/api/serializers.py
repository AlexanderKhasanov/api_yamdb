from rest_framework import serializers
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.utils import timezone

from reviews.models import Review, Comment, Title, Genre, Category, TitleGenre

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                'Использование имя "me" в качестве username запрещено.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "pub_date",
        )


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class TitleGetSerializers(serializers.ModelSerializer):
    genre = GenreSerializers(many=True)
    category = CategorySerializers()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ("id", "name", "year", "rating", "description", "genre",
                  "category")

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(rating=Avg("score"))
        if rating.get("rating") is None:
            return None
        return round(rating.get("rating"))


class TitleSerializers(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")

    def create(self, validated_data):
        genres = validated_data.pop("genre")
        title = Title.objects.create(**validated_data)
        TitleGenre.objects.bulk_create(
            [TitleGenre(title=title, genre=genre) for genre in genres]
        )
        return title

    def validate_year(self, value):
        max_year = timezone.now().year
        if value > max_year:
            raise serializers.ValidationError(
                "Год выхода произведения не может быть больше текущего года"
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
