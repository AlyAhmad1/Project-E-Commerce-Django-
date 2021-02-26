import django_filters
from .models import Item


class ABC(django_filters.FilterSet):
    Search = django_filters.CharFilter(required=True,field_name='title', lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ''
