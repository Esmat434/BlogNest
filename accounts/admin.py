from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, AccountVerified, PasswordReset

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "status",
        "country",
        "city",
        "email_verified",
        "is_superuser",
        "is_active",
    ]

    list_filter = ["email", "username", "country", "city"]
    search_fields = ["email", "username", "first_name", "last_name", "country", "city"]
    ordering = ["email", "username", "country", "city"]

    fieldsets = (
        (None, {"fields": ("username", "email", "password", "last_login_ip")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "picture",
                    "country",
                    "city",
                    "phone_number",
                    "birth_date",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "email_verified",
                    "status",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            "Registrations",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password",
                    "last_login_ip",
                    "first_name",
                    "last_name",
                    "address1",
                    "address2",
                    "phone_number",
                    "country",
                    "city",
                    "birth_date",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "email_verified",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    list_filter = ["user"]
    search_fields = ["user"]
    ordering = ["user"]


@admin.register(AccountVerified)
class AccountVerifiedAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "token", "created_time"]
    list_filter = ["user"]
    search_fields = ["user"]
    ordering = ["user"]


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "token", "created_time"]
    list_filter = ["user"]
    search_fields = ["user"]
    ordering = ["user"]
