import django_filters
from reviews.models import Title, Genre, Category


class TitleFilters(django_filters.FilterSet):
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name="genre__slug",
        to_field_name="slug",
        queryset=Genre.objects.all()
    )
    category = django_filters.ModelChoiceFilter(
        to_field_name="slug", queryset=Category.objects.all()
    )
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ("year",)
