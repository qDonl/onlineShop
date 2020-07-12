from django.db.models import Q
from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class ThirdCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    """第二级分类"""

    sub_cat = ThirdCategorySerializer(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer(serializers.ModelSerializer):
    """第一级分类"""
    sub_cat = SubCategorySerializer(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexGoodsCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = SubCategorySerializer(many=True)

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.pk) |
                                         Q(category__parent_category_id=obj.pk) |
                                         Q(category__parent_category__parent_category_id=obj.pk))
        serializer = GoodsSerializer(all_goods, many=True)
        return serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
