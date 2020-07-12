import re
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers

User = get_user_model()


class SmsSerializers(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11,
                                   error_messages={
                                       "max_length": "手机格式错误",
                                       "min_length": "手机格式错误",
                                   })

    def validate_mobile(self, mobile):
        """手机号验证"""
        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError("请输入正确格式的手机号码")

        exist = User.objects.filter(mobile=mobile).exists()
        if exist:
            raise serializers.ValidationError("该手机号已被注册")

        return mobile


class RegisterSerializer(serializers.ModelSerializer):
    """用户注册"""
    code = serializers.CharField(max_length=4, min_length=4, write_only=True,
                                 error_messages={
                                     "min_length": "验证码错误",
                                     "max_length": "验证码错误",
                                     "non_field_errors": "验证码已过期*"
                                 })
    username = serializers.CharField(max_length=11, min_length=11,
                                     error_messages={
                                         "blank": "请输入手机号码",
                                         "min_length": "手机格式错误",
                                         "max_length": "手机格式错误",
                                     })
    password = serializers.CharField(max_length=16, min_length=6, style={'input_type': 'password'},
                                     error_messages={
                                         "blank": "请输入密码",
                                         "min_length": "密码至少6位",
                                         "max_length": "密码最长16位",
                                     })

    def validate(self, data):
        mobile = data.get("username")

        cache_code = cache.get(mobile, None)
        if not cache_code:
            raise serializers.ValidationError("验证码已过期")

        f_code = data.get("code")
        if f_code != cache_code:
            raise serializers.ValidationError("验证码错误")

        data['mobile'] = data['username']
        del data['code']
        return data

    class Meta:
        model = User
        fields = ("mobile", "password", "code", "username")


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("name", "birthday", "email", "gender", "mobile")
