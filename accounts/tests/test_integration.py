import uuid
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, AccountVerified, PasswordForgotResetToken


class AccountInegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="test1",
            email="test1@gmail.com",
            password="1234",
            phone_number="+93664420001",
        )
        self.client.login(username="test1", password="1234")
        self.accountVerified = AccountVerified.objects.create(
            user=self.user, token=uuid.uuid4()
        )
        self.reset_token = PasswordForgotResetToken.objects.create(user=self.user)

    def test_get_signin_view_integration(self):
        respnse = self.client.get(reverse("signin"))
        self.assertEqual(respnse.status_code, 200)
        self.assertTemplateUsed(respnse, "Account/signin.html")

    def test_post_signin_view_integration(self):
        response = self.client.post(
            reverse("signin"), data={"username": "test1", "password": "1234"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_post_signin_view_user_not_exists_integration(self):
        response = self.client.post(
            reverse("signin"), data={"username": "testuser", "password": "101012"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/signin.html")
        self.assertContains(response, "User does not exists")
        self.assertIn("error", response.context)
        self.assertEqual(response.context["error"], "User does not exists.")

    def test_post_signin_view_incorrect_password_integration(self):
        response = self.client.post(
            reverse("signin"), data={"username": "test1", "password": "39803290"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/signin.html")
        self.assertContains(response, "Incorrect password!")
        self.assertIn("error", response.context)
        self.assertEqual(response.context["error"], "Incorrect password!")

    def test_get_confirm_signin_view_integration(self):
        response = self.client.get(reverse("Suspicious_Activity", args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_get_signout_view_integration(self):
        response = self.client.get(reverse("signout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/signout.html")

    def test_post_signout_view_integration(self):
        response = self.client.post(reverse("signout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_get_account_verified_view_correct_integration(self):
        response = self.client.get(
            reverse("account-verified", args=[self.accountVerified.token])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_get_account_verified_view_incorrect_integration(self):
        response = self.client.get(reverse("account-verified", args=[uuid.uuid4()]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "token does not exists")

    def test_get_passwordforgot_view_integration(self):
        response = self.client.get(
            reverse("password-forgot", args=[self.reset_token.token])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/passwordReset.html")

    def test_post_passwordforgot_view_correct_integration(self):
        response = self.client.post(
            reverse("password-forgot", args=[self.reset_token.token]),
            data={"new_password": "12345", "confirm_password": "12345"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_post_passwordforgot_view_incorrect_integration(self):
        response = self.client.post(
            reverse("password-forgot", args=[self.reset_token.token]),
            data={"new_password": "123456", "confirm_password": "12345"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/passwordForgot.html")
        self.assertIn("error", response.context)
        self.assertEqual(response.context["error"], "Passwords do not match.")

    def test_get_profile_view_integration(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/profile.html")
        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"], self.user)

    def test_get_editprofile_view_integration(self):
        response = self.client.get(reverse("profile-edit"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/profileEdit.html")
        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"], self.user)

    def test_post_editprofile_view_integration(self):
        response = self.client.post(
            reverse("profile-edit"),
            data={
                "first_name": "ajmal",
                "last_name": "mohammadi",
                "email": "ajmal@gmail.com",
                "password1": "12345",
                "password2": "12345",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("profile"), fetch_redirect_response=False
        )

    def test_post_editprofile_view_password_incorrect_integration(self):
        response = self.client.post(
            reverse("profile-edit"),
            data={
                "first_name": "ajmal",
                "last_name": "mohammadi",
                "email": "ajmal@gmail.com",
                "password1": "12345",
                "password2": "1234590",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/profileEdit.html")
        self.assertIn("user", response.context)
        self.assertIn("error", response.context)
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(response.context["error"], "Passwords do not match")

    def test_get_delete_account_view_integration(self):
        response = self.client.get(reverse("delete-account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Account/deleteAccount.html")

    def test_post_delete_account_view_integration(self):
        response = self.client.post(reverse("delete-account"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
