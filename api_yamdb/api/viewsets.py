from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListCreateDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                              mixins.DestroyModelMixin, GenericViewSet):
    lookup_field = 'slug'
    lookup_value_regex = '[-a-zA-Z0-9_]+'
