from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from user import views
from user.views import (
    LoginApi,
    UserListing
)

router = DefaultRouter()
router.register("login", LoginApi, basename="Login API")
router.register("vendor-notery-list", UserListing, basename="User List")


urlpatterns = [
    # path('', views.home, name='home')
] + router.urls
