from django.test import TestCase, Client
from django.urls import reverse


class AccountsRedirectUrlsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_confirm_signin_redirect_url_correct(self):
        response = self.client.get(reverse("Suspicious_Activity", args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_signout_redirect_url_correct(self):
        response = self.client.get(reverse("signout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_profile_redirect_url_correct(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_editprofile_redirect_url_correct(self):
        response = self.client.get(reverse("profile-edit"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_delete_account_redirect_url_correct(self):
        response = self.client.get(reverse("delete-account"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))
