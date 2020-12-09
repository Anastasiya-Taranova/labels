from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("applications.index.urls")),
    path("sentry-debug/", lambda _r: 1/0),
    path("accounts/", include("allauth.urls")),
]
