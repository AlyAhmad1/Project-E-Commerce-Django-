import django_filters
from .models import Item


class ABC(django_filters.FilterSet):
    Search = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Search')

    class Meta:
        model = Item
        fields = ''
