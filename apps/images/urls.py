from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# drf-yasg schema_view settings

schema_view = get_schema_view(
    openapi.Info(
        title="Images API",
        default_version='v1',
        description="API documentation for the images upload application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'images', ImageViewSet)


urlpatterns = [
    path('', include(router.urls)),

    # swagger urls
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
