from django.test import SimpleTestCase, Client
from django.urls import reverse


class DashboardRedirectUrlTestCase(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_report_url_correct(self):
        response = self.client.get(reverse("report"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signin/")

    def test_post_list_report_redirect_url_correct(self):
        response = self.client.get(reverse("post_list_report"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signin/")

    def test_post_detail_report_redirect_url_correct(self):
        response = self.client.get(reverse("post_detail_report", args=[12]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signin/")

    def test_media_library_report_redirect_url_correct(self):
        response = self.client.get(reverse("media_library_report"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signin/")

    def test_comment_report_redirect_url_correct(self):
        response = self.client.get(reverse("comment_report"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signin/")

    def test_follower_report_redirect_url_correct(self):
        response = self.client.get(reverse("follower_report"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signin/")

    def test_followed_report_redirect_url_correct(self):
        response = self.client.get(reverse("followed_report"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signin/")

    def test_unfollow_redirect_url_correct(self):
        response = self.client.get(reverse("un_follow", args=[10]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signin/")
