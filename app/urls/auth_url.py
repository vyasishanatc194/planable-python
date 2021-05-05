# -*- coding: utf-8 -*-
from django.urls import path
from .. import views


urlpatterns = [
    path("signup/", views.SignUpApiView.as_view(), name="signup"),
    path("cities/", views.CityListingAPIView.as_view(), name="cities"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path("plan/", views.PlanCreateAPIView.as_view(), name="plan"),
    path("categories/", views.CategoryListingAPIView.as_view(), name="categories"),
    # path("connect-instagram/", views.SaveInstagramTokenAPI.as_view(), name="connect-instagram"),
    # path("disconnect-instagram/", views.SaveInstagramTokenAPI.as_view(), name="disconnect-instagram"),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('instagram/connect/', views.auth.ConnectInstagramAPI.as_view(), name='instagram-connect'),
    path('instagram/disconnect/', views.auth.DisconnectInstagramAPI.as_view(), name='instagram-disconnect'),
]
