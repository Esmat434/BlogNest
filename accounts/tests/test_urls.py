from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, PasswordForgotResetToken

# Create your tests here.


class AccoutnUrlsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="12345",
            phone_number="+93884450002",
        )
        self.client.login(username="testuser", password="12345")
        self.reset_token = PasswordForgotResetToken.objects.create(user=self.user)

    def test_url_signup_exists(self):
        response = self.client.get(reverse("signup"))
        return self.assertEqual(response.status_code, 200)

    def test_url_signin_exists(self):
        response = self.client.get(reverse("signin"))
        self.assertEqual(response.status_code, 200)

    def test_url_signout_redirect(self):
        response = self.client.get(reverse("signout"))
        self.assertEqual(response.status_code, 200)

    def test_url_passwordForgot_exists(self):
        response = self.client.get(
            reverse("password-forgot", args=[self.reset_token.token])
        )
        self.assertEqual(response.status_code, 200)

    def test_url_passwordForgotResetToken_exists(self):
        response = self.client.get(reverse("password-forgot-reset-token"))
        self.assertEqual(response.status_code, 200)

    def test_url_profile_exists(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_url_profileEdit_exists(self):
        response = self.client.get(reverse("profile-edit"))
        self.assertEqual(response.status_code, 200)

    def test_url_delete_account_exists(self):
        response = self.client.get(reverse("delete-account"))
        self.assertEqual(response.status_code, 200)
