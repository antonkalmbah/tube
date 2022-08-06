from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from rest_framework import permissions  # Для динамической подготовки документации
from drf_yasg.views import get_schema_view  # Для динамической подготовки документации
from drf_yasg import openapi  # Для динамической подготовки документации

from config.settings import MEDIA_URL
from config.settings import MEDIA_ROOT


schema_view = get_schema_view(  # Схема для UI документации
    openapi.Info(
        title="VH API",
        default_version="v1",
        description="DRF for video hosting Frond-end",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ilya.dianburgskiy@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('comments_and_chats.urls')),
    path('api/v1/', include('media_storage.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    # Для настройки подключения авторизации подключаем роутинг
    path('api/v1/dj-rest-auth/registration/',
         include('dj_rest_auth.registration.urls')),  # Для подключения all-auth для регистрации пользователей

    path('swagger/', schema_view.with_ui(  # Формат документации Swagger
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(  # Формат документации ReDoc
        'redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^webpush/', include('webpush.urls')),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
