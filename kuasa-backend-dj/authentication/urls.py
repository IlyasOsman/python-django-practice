from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UserRegistrationView,
    UserLoginView,
    LeadershipUserViewSet,
    UserListView,
    UserProfileView,
    UserDetailView,
    UserProfileImageView,
    VerifyEmailView,
)


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("leaders/", LeadershipUserViewSet.as_view({"get": "list"}), name="leaders"),
    path("members/", UserListView.as_view(), name="members"),
    path("members/<int:pk>/", UserDetailView.as_view(), name="members_detail"),
    path(
        "profile/",
        UserProfileView.as_view({"get": "retrieve", "patch": "update"}),
        name="profile",
    ),
    path(
        "profile/image/upload/",
        UserProfileImageView.as_view({"post": "upload_image"}),
        name="profile-upload-image",
    ),
    path(
        "profile/image/remove/",
        UserProfileImageView.as_view({"post": "remove_image"}),
        name="profile-remove-image",
    ),
    path(
        "profile/change_password/",
        UserProfileView.as_view({"post": "change_password"}),
        name="change_password",
    ),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]
