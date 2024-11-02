from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Регистрация пользователя
    """

    queryset = User.objects.all()
    model = User
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = UserSerializer
