from django.test import TestCase, Client
from accounts.models import *


class AccountModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="123456",
            phone_number="+93445567816",
        )
        self.client.login(username="testuser", password="123456")
        self.profile = Profile.objects.create(user=self.user)
        self.accountVerified = AccountVerified.objects.create(user=self.user)
        self.passwordReset = PasswordReset.objects.create(user=self.user)
        self.reset_token = PasswordForgotResetToken.objects.create(user=self.user)

    def test_customuser_model(self):
        self.assertEqual(self.user.username, "testuser")

    def test_profile_mode(self):
        self.assertEqual(self.profile.user.username, "testuser")

    def test_accountVerified_model(self):
        self.assertEqual(self.accountVerified.user.username, "testuser")

    def test_passwordReset(self):
        self.assertEqual(self.passwordReset.user.username, "testuser")

    def test_passwordForgotResetToken(self):
        self.assertEqual(self.reset_token.user, self.user)
