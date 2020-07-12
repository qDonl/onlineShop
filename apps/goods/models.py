from django.db import models

from utils.models import BaseModel
from DjangoUeditor.models import UEditorField


class GoodsCategory(BaseModel):
    """商品类别"""
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(null=True, blank=True, max_length=30, verbose_name="类别名")
    code = models.CharField(null=True, blank=True, max_length=30, verbose_name="类别code")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别")
    desc = models.TextField(null=True, blank=True, verbose_name="类别描述")
    parent_category = models.ForeignKey("self", models.CASCADE, null=True, blank=True, verbose_name="父类目级别",
                                        related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(BaseModel):
    """品牌名"""
    category = models.ForeignKey(GoodsCategory, models.CASCADE, related_name='brands', null=True, blank=True,
                                 verbose_name="商品类目")
    name = models.CharField(null=True, blank=True, max_length=30, verbose_name="品牌名")
    desc = models.TextField(null=True, blank=True, max_length=200, verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """商品"""
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类目", on_delete=models.CASCADE)
    goods_sn = models.CharField(max_length=50, null=True, blank=True, verbose_name="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述")
    goods_desc = UEditorField(verbose_name="内容", imagePath="goods/images/", width=1000, height=300,
                              filePath="goods/files/", default='')
    ship_free = models.BooleanField(default=True, verbose_name="是否包邮")
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexAd(BaseModel):
    category = models.ForeignKey(GoodsCategory, related_name='category', on_delete=models.CASCADE, verbose_name="商品类目")
    goods = models.ForeignKey(Goods, related_name='goods', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '首页商品类别广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsImage(BaseModel):
    """商品轮播图"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", related_name="images")
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(BaseModel):
    """轮播的商品"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    image = models.ImageField(upload_to='banner/', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(BaseModel):
    """热搜词"""
    keywords = models.CharField(null=True, blank=True, max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
