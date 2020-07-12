from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from goods.filters import GoodsFilters
from goods.models import Goods, GoodsCategory, Banner
from goods.serializers import (
    GoodsSerializer,
    GoodsCategorySerializer,
    BannerSerializer,
    IndexGoodsCategorySerializer
)
from utils.help import CustomPagination


class GoodsListViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    list: 商品列表
    retrieve: 商品详情
    """
    queryset = Goods.objects.all()
    pagination_class = CustomPagination
    serializer_class = GoodsSerializer
    filter_class = GoodsFilters
    # authentication_classes = [JSONWebTokenAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "shop_price"]
    search_fields = ("name", "goods_desc")
    ordering_fields = ['shop_price', 'sold_nums']


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    list: 分类列表
    retrieve: 分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()[:5]


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.all()
    serializer_class = IndexGoodsCategorySerializer
