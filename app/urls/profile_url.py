# -*- coding: utf-8 -*-
from django.urls import path
from .. import views


urlpatterns = [

    path("add-image/", views.ProfileImageAPIView.as_view(), name="add-image"),
    path("remove-image/<int:pk>/", views.ProfileImageAPIView.as_view(), name="remove-image"),

    path("profile/", views.UserProfileAPIView.as_view(), name="profile"),
    path("view-profile/<int:pk>/", views.ViewProfileAPIView.as_view(), name="view-profile"),
]