import time
from uuid import uuid4

from django.conf import settings
from rest_framework import serializers

from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from utils.alipay import AliPay


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all())
    nums = serializers.IntegerField(min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于1",
                                        "required": "请选择商品数量"
                                    })

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data.get("nums")
        goods = validated_data.get("goods")

        shoppingCart = ShoppingCart.objects.filter(user=user, goods=goods)
        # 是否已有记录
        if shoppingCart:
            # 已存在数据: 商品数量增加
            shoppingCart = shoppingCart[0]
            shoppingCart.nums += nums
            shoppingCart.save()
        else:
            # 若没有: 添加商品信息
            shoppingCart = shoppingCart.create(**validated_data)
        return shoppingCart

    def update(self, instance, validated_data):
        instance.nums = validated_data.get('nums')
        instance.save()
        return instance


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(default="paying", read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    alipay_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016102300744540",
            app_notify_url="http://47.96.8.228:8020/alipay/return/",
            app_private_key_path=settings.PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.96.8.228:8020/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def generate_order_sn(self):
        """生成订单号: 当前时间+userId"""
        return f"{time.strftime('%Y%m%d%H%M%S')}{self.context['request'].user.mobile}"

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016102300744540",
            app_notify_url="http://47.96.8.228:8020/alipay/return/",
            app_private_key_path=settings.PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.96.8.228:8020/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"
