from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .serializers import CollectionsSerializer
from .models import Collections


class CollectionsViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = CollectionsSerializer
    queryset = Collections.objects.all()
    filter_backends = (OrderingFilter, )
    ordering = ('-create_at',)
