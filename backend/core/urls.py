from django.contrib import admin, auth
from django.urls import path, include

from django.contrib.auth import views as auth_views

from django.views.generic import RedirectView
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    path("", views.ItemListView.as_view(), name="item-list"),
    path("create/", views.ItemCreateView.as_view(), name="item-create"),
    # path("", include("social_django.urls", namespace="social")),
    # path("auth/", include("rest_framework_social_oauth2.urls")),
]

app_name = "core"
