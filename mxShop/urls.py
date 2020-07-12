from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include
from django.views.generic import TemplateView
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token


import xadmin
from goods.views import (
    GoodsListViewSet,
    CategoryViewSet,
    BannerViewSet,
    IndexCategoryViewSet)
from user_operation.views import (
    UserFavViewSet,
    LeavingMessageViewSet,
    AddressViewSet)
from trade.views import (
    ShoppingCartViewSet,
    OrderInfoViewSet,
    AliPayViewSet)
from users.views import SmsCodeViewSet, UserViewSet

router = DefaultRouter()

# 前端 获取数据 API
router.register("goods", GoodsListViewSet, basename="goods")
router.register("categories", CategoryViewSet, basename="categories")
router.register("codes", SmsCodeViewSet, basename="codes")
router.register("users", UserViewSet, basename="users")
router.register("userfavs", UserFavViewSet, basename="userfavs")
router.register("messages", LeavingMessageViewSet, basename="messages")
router.register("address", AddressViewSet, basename="address")
router.register("shopcarts", ShoppingCartViewSet, basename="shopcarts")
router.register("orders", OrderInfoViewSet, basename="orders")
router.register("banners", BannerViewSet, basename="banners")
router.register("indexgoods", IndexCategoryViewSet, basename="indexgoods")

urlpatterns = [
    url(r"^xadmin/", xadmin.site.urls),
    url(r"^docs/", include_docs_urls(title="生鲜超市")),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^index/", TemplateView.as_view(template_name="index.html"), name="index"),

    # django REST framework 自带Token认证
    url(r"^api-token-auth/", views.obtain_auth_token),
    # 使用JWT（Json Web Token）实现用户登录认证
    url(r"^login/$", obtain_jwt_token),
    url(r"^alipay/return/", AliPayViewSet.as_view(), name="alipay"),

    url(r"^", include(router.urls)),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
