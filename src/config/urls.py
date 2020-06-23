from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from common.views import home_page

schema_view = get_schema_view(
    openapi.Info(
        title="Starnavi API",
        default_version="v1",
        description="""All endpoints in Starnavi API are described here.
        The `swagger-ui` view can be found [here](/api/docs/).
        The `ReDoc` view can be found [here](/api/redocs/).""",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path("admin/", admin.site.urls),
    # User management
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("", home_page, name="homepage"),
    path("", include("allauth.urls")),
    # API
    path("api/", include("apps.api.urls", namespace="api_v1_starnavi")),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="docs_api_v1_view",
    ),
    # path(
    #     "api/redocs/",
    #     schema_view.with_ui("redoc", cache_timeout=0),
    #     name="redocs_api_v1_view",
    # ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
