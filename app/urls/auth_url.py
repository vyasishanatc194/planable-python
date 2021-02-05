# -*- coding: utf-8 -*-
from django.urls import path
from .. import views


urlpatterns = [
    path("signup/", views.SignUpApiView.as_view(), name="signup"),
    path("cities/", views.CityListingAPIView.as_view(), name="cities"),
]