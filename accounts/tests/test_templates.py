from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, PasswordForgotResetToken


class AccountTemplatesTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="1234",
            phone_number="+93662220017",
        )
        self.client.login(username="testuser", password="1234")
        self.reset_token = PasswordForgotResetToken.objects.create(user=self.user)

    def test_signupt_template_exists(self):
        response = self.client.get(reverse("signup"))
        self.assertTemplateUsed(response, "Account/signup.html")

    def test_signin_tepmlate_exists(self):
        response = self.client.get(reverse("signin"))
        self.assertTemplateUsed(response, "Account/signin.html")

    def test_signout_template_exists(self):
        response = self.client.get(reverse("signout"))
        self.assertTemplateUsed(response, "Account/signout.html")

    def test_passwordForgot_template_exists(self):
        response = self.client.get(reverse("password-forgot-reset-token"))
        self.assertTemplateUsed(response, "Account/passwordForgot.html")

    def test_passwordForgot_template_exists(self):
        response = self.client.get(
            reverse("password-forgot", args=[self.reset_token.token])
        )
        self.assertTemplateUsed(response, "Account/passwordReset.html")

    def test_profile_template_exists(self):
        response = self.client.get(reverse("profile"))
        self.assertTemplateUsed(response, "Account/profile.html")

    def test_profileEdit_template_exists(self):
        response = self.client.get(reverse("profile-edit"))
        self.assertTemplateUsed(response, "Account/profileEdit.html")

    def test_delete_account_template_exists(self):
        response = self.client.get(reverse("delete-account"))
        self.assertTemplateUsed(response, "Account/deleteAccount.html")
