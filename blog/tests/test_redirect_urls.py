from django.test import SimpleTestCase, Client
from django.urls import reverse


class BlogRedirectUrlTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_post_create_view_redirect_url_correct(self):
        response = self.client.get(reverse("post-create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_post_detail_view_redirect_url_correct(self):
        response = self.client.get(reverse("post-detail", args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_post_update_view_redirect_url_correct(self):
        response = self.client.get(reverse("post-update", args=[2]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_post_delete_view_redirect_url_correct(self):
        response = self.client.get(reverse("post-delete", args=[3]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_notification_post_view_redirect_url_correct(self):
        response = self.client.get(reverse("post-notification"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))
