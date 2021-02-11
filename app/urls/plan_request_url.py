# -*- coding: utf-8 -*-
from django.urls import path
from .. import views


urlpatterns = [
    path("join-plan/", views.PlanJoiningRequestAPIView.as_view(), name="join-plan"),
    path("plan-request/<int:pk>/", views.AcceptDeclineJoiningRequestAPIView.as_view(), name="plan-request"),
]
