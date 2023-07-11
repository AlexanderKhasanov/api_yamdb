from rest_framework import viewsets
from rest_framework import mixins


class CreateModelViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet
):
    pass
