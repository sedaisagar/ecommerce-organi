import django_filters

from products.models import Product
from django.db.models import Q

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="custom_search")
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['search', 'name']

    def custom_search(self, queryset, name, value):
        values = value.split(" ")
        query_filter = Q()

        for word in values:
            if word:
               query_filter |= Q(name__icontains=word) | Q(description__icontains=word) | Q(short_description__icontains=word) | Q(information__icontains=word)

        return queryset.filter(query_filter)