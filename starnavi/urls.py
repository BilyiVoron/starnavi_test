from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from starnavi.swagger import get_swagger_view

docs_api_view = get_swagger_view(title="Docs API")

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path("admin/", admin.site.urls),
    # User management
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    # path("", home_page, name="homepage"),
    path("", include("allauth.urls")),
    # API
    path("api/docs/", docs_api_view, name="docs_api"),
    path("api/", include("api.urls", namespace="api_v1_starnavi")),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
