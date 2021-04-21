# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import auth_url, profile_url, plan_url, plan_request_url

app_name = "user"

urlpatterns = [
    path("", include(auth_url)),
    path("", include(profile_url)),
    path("", include(plan_url)),
    path("", include(plan_request_url)),
    path("accounts/", include("allauth.urls")),
]
