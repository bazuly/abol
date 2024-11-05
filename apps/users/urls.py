from django.urls import path
from .views import CreateUserView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    # user api routes
    path('user_api', CreateUserView.as_view(), name='user_api'),

    # simple jwt routes
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
