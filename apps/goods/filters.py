import django_filters
from django.db.models import Q

from goods.models import Goods


class GoodsFilters(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter("shop_price", "gte")
    pricemax = django_filters.NumberFilter("shop_price", "lte")
    top_category = django_filters.NumberFilter(method="top_category_filter")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) |
                               Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', "pricemax", "is_hot", "is_new"]
