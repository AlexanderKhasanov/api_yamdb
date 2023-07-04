from rest_framework import serializers
from reviews.models import Title


class TitleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')