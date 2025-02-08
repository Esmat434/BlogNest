from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from accounts.signupForm import SignupForm


class AccountsContextDataTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_signup_context_data_correct(self):
        response = self.client.get(reverse("signup"))
        self.assertIsInstance(response.context["form"], SignupForm)
