from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", include("web.urls")),
    path("admin/", admin.site.urls),
]