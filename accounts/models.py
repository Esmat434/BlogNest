from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django_countries.fields import CountryField
from django.utils.timezone import now
from uuid import uuid4
from datetime import timedelta

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("status", "Admin")
        extra_fields.setdefault("first_name", "Esmatullah")
        extra_fields.setdefault("last_name", "Hadel")
        extra_fields.setdefault("country", "Afghanistan")
        extra_fields.setdefault("city", "Kabul")
        extra_fields.setdefault("email_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    CHOICE = (
        ("Admin", "Admin"),
        ("Editor", "Editor"),
        ("Authore", "Authore"),
        ("User", "User"),
    )
    status = models.CharField(max_length=50, default="User", choices=CHOICE)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    picture = models.FileField(upload_to="images/profile", blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
    country = CountryField()
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100, default="")
    birth_date = models.DateTimeField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

    objects = UserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class AccountVerified(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4)
    created_time = models.DateTimeField(auto_now_add=True)


class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4)
    created_time = models.DateTimeField(auto_now_add=True)


class PasswordForgotResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4)
    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return now() > self.created_time + timedelta(minutes=3)
