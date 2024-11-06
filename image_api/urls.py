from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.image_service.urls')),
    path('users/', include('apps.users.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)


# остались тесты, поделить нормально ответственно во вьюхах,
# написать трай эксепты с обработкой ошибок
# написать readme.md
# кеширование получение изображений с помощью redis
# и создать асинхронный один эндпоинт
