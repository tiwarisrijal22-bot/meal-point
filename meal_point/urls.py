from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from meal_app.views import create_admin


urlpatterns = [
    path("admin/", admin.site.urls),
    path("create-admin/", create_admin),
    path("", include("meal_app.app_urls")),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
