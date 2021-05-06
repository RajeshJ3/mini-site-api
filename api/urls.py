from django.contrib import admin
from django.urls import path, re_path, include

# Swagger
from rest_framework import permissions, authentication
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API docs.",
        default_version='v1',
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
    authentication_classes=(authentication.TokenAuthentication, authentication.SessionAuthentication)
)


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/improvements/', include('improvements.urls')),

    re_path(r'^api/swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]