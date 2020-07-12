from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

User = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 100


class AuthenticationBackend(ModelBackend):
    """自定义用户认证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except ModuleNotFoundError as e:
            return None
