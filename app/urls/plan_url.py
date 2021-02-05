# -*- coding: utf-8 -*-
from django.urls import path
from .. import views


urlpatterns = [
    path("plan/", views.PlanCreateAPIView.as_view(), name="plan"),
    path("plan/<int:pk>/", views.PlanDetailAPIView.as_view(), name="plan-detail"),


    path("categories/", views.CategoryListingAPIView.as_view(), name="categories"),

    path("postal-codes/", views.PostalCodeListingAPIView.as_view(), name="postal-codes"),
]