from string import digits

from django.contrib.auth import get_user_model
from django.core.cache import cache
from random import choices
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.serializers import SmsSerializers, RegisterSerializer, UserDetailSerializer

User = get_user_model()


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create: 发送短信验证码
    """

    serializer_class = SmsSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 从验证的数据中获取 手机号 mobile
        mobile = serializer.validated_data.get('mobile')
        # 生成4位数字验证码
        code = "".join(choices(digits, k=4))
        # 将生成的手机验证码和手机号码保存到缓存中 {mobile: code}
        cache.set(mobile, code, 5 * 60)
        # 模仿发送手机验证码
        print(f"{mobile} -> {code}")
        data = {"mobile": mobile}
        return Response(data, status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    # """用户注册、登录"""
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_permissions(self):
        if self.action == "retrieve":
            # 写成实例形式 IsAuthenticated()
            return [IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        """用户注册， 创建一个新的用户"""
        # 将获取的数据进行序列化
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 将用户提交的数据保存到数据库当中
        user = self.perform_create(serializer)

        # 用户注册成功， 执行登录操作
        data = serializer.data
        payload = jwt_payload_handler(user)
        data['token'] = jwt_encode_handler(payload)
        data['name'] = user.__str__()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        # retrieve 用户登录操作
        if self.action == "retrieve":
            return UserDetailSerializer

        # 用户注册操作
        elif self.action == "create":
            return RegisterSerializer
        return UserDetailSerializer
