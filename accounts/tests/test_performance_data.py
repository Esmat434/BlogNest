from django.test import TestCase, Client
from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext
from accounts.models import CustomUser, AccountVerified, PasswordForgotResetToken
import uuid


class AccountPerformanceDataTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="1234",
            phone_number="+93771270040",
        )
        self.client.login(username="testuser", password="1234")
        self.account_verified = AccountVerified(user=self.user, token=uuid.uuid4())
        self.reset_token = PasswordForgotResetToken.objects.create(user=self.user)

    def test_signin_perfomance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.post(
                reverse("signin"), data={"username": "testuser", "password": "1234"}
            )
        print(f"CustomUser From Signin View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 11)

    def test_lock_account_on_suspicious_activity_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(
                reverse("Suspicious_Activity", args=[self.user.pk])
            )
        print(
            f"CustomUser From Lock_Account_on_Suspicious_Activity View Total Queries: {len(queries)}"
        )
        self.assertLessEqual(len(queries), 7)

    def test_accountverified_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(
                reverse("account-verified", args=[self.account_verified.token])
            )
        print(f"Account Verified Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 6)

    def test_passwordforgot_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(
                reverse("password-forgot", args=[self.reset_token.token])
            )
        print(f"CustomUser From PasswordForgot View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 6)

    def test_passwordForgotResetToken_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("password-forgot-reset-token"))
        print(
            f"CustomUser From PasswordForgotResetToken View Total Queries: {len(queries)}"
        )
        self.assertLessEqual(len(queries), 5)

    def test_profile_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("profile"))
        print(f"CustomUser From Profile View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 6)

    def test_editprofile_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("profile-edit"))
        print(f"CustomUser From ProfileEdit View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 6)

    def test_deleteaccount_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("delete-account"))
        print(f"CustomUser From DeleteAccount View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 5)
