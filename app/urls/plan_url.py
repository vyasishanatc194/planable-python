# -*- coding: utf-8 -*-
from django.urls import path
from .. import views


urlpatterns = [
    path("plan/", views.PlanCreateAPIView.as_view(), name="plan"),
    path("plan/<int:pk>/", views.PlanDetailAPIView.as_view(), name="plan-detail"),
    path("plans/", views.PlanListingAPIView.as_view(), name="plans"),
    path(
        "my-created-plans/",
        views.MyPlanListingAPIView.as_view(),
        name="my-created-plans",
    ),
    path("categories/", views.CategoryListingAPIView.as_view(), name="categories"),
    path(
        "postal-codes/", views.PostalCodeListingAPIView.as_view(), name="postal-codes"
    ),
    path("home-plans/", views.HomePlanListingAPIView.as_view(), name="home-plans"),
    
]
