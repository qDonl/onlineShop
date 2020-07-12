from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.conf import settings

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import (
    ShoppingCartSerializer,
    ShoppingCartDetailSerializer,
    OrderInfoSerializer,
    OrderDetailSerializer)
from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from datetime import datetime
from django.shortcuts import redirect


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    list: 购物车列表
    create: 添加购物车
    delete: 删除商品
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCartSerializer
    lookup_field = "goods_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ShoppingCartSerializer
        elif self.action == 'detail':
            return ShoppingCartDetailSerializer
        return ShoppingCartDetailSerializer


class OrderInfoViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderInfoSerializer

    def perform_create(self, serializer):
        # 保存当前订单
        order = serializer.save()
        # 获取所有的购物车商品
        shopCarts = ShoppingCart.objects.filter(user=self.request.user)

        # 保存所有的订单商品信息
        for shopCart in shopCarts:
            orderGoods = OrderGoods()
            orderGoods.goods = shopCart.goods
            orderGoods.goods_num = shopCart.nums
            orderGoods.order = order
            orderGoods.save()

            # 清空购物车
            shopCart.delete()
        return order


class AliPayViewSet(APIView):
    """支付接口实现"""

    def get(self, request):
        """
        处理支付 return_url
        :param request:
        :return:
        """
        processed_dict = {key: value for key, value in request.GET.items()}

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016102300744540",
            app_notify_url="http://47.96.8.228:8020/alipay/return/",
            app_private_key_path=settings.PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.96.8.228:8020/alipay/return/"
        )
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", "TRADE_SUCCESS")

            orderInfo = OrderInfo.objects.filter(order_sn=order_sn)
            for order in orderInfo:
                order.pay_status = trade_status
                order.trade_no = trade_no
                order.pay_time = datetime.now()
                order.save()

            resp = redirect("index")
            # 支付完成跳转到 pay/页面
            resp.set_cookie("nextPath", "pay", max_age=2)
            print("成功")
            return resp
        else:
            print("失败")
            resp = redirect("index")
            return resp

    def post(self, request):
        """
        处理notify_url
        :param request:
        :return:
        """
        processed_dict = {key: value for key, value in request.POST.items()}

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016102300744540",
            app_notify_url="http://47.96.8.228:8020/alipay/return/",
            app_private_key_path=settings.PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.96.8.228:8020/alipay/return/"
        )
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", None)

            orderInfo = OrderInfo.objects.filter(order_sn=order_sn)
            for order in orderInfo:
                order.pay_status = trade_status
                order.trade_no = trade_no
                order.pay_time = datetime.now()
                order.save()
            return Response("success")
