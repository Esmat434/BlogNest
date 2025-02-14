from django.urls import path
from .views import (
    SignupView,
    SigninView,
    SignoutView,
    AccountVerifiedView,
    PasswordForgotResetTokenView,
    PasswordForgotResetView,
    ProfileView,
    ProfileEditView,
    Lock_Account_on_Suspicious_Activity_View,
    DeleteAccountView,
    SettingsView,
)

app_name = "accounts"
urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    path(
        "condfirm-signin/<int:pk>/",
        Lock_Account_on_Suspicious_Activity_View.as_view(),
        name="Suspicious_Activity",
    ),
    path("signout/", SignoutView.as_view(), name="signout"),
    path(
        "account-verified/<uuid:token>/",
        AccountVerifiedView.as_view(),
        name="account-verified",
    ),
    path(
        "password-forgot/",
        PasswordForgotResetTokenView.as_view(),
        name="password-forgot-reset-token",
    ),
    path(
        "password-forgot/<uuid:token>/",
        PasswordForgotResetView.as_view(),
        name="password-forgot",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile-edit"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
    path("settings/", SettingsView.as_view(), name="settings"),
]
