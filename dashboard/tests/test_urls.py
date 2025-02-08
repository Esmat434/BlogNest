from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from blog.models import Post, Follow


class DashboardUrlTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="1234",
            phone_number="+93771420009",
        )

        self.user2 = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="12345",
            phone_number="+93771680003",
        )

        self.client.login(username="testuser", password="1234")

        self.post = Post.objects.create(
            author=self.user, title="test post", content="test content"
        )

        self.follow = Follow.objects.create(follower=self.user, followee=self.user2)

    def test_report_url_correct(self):
        response = self.client.get(reverse("report"))
        self.assertEqual(response.status_code, 200)

    def test_post_list_report_url_correct(self):
        response = self.client.get(reverse("post_list_report"))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_report_url_correct(self):
        response = self.client.get(reverse("post_detail_report", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_media_library_report_url_exists(self):
        response = self.client.get(reverse("media_library_report"))
        self.assertEqual(response.status_code, 200)

    def test_comment_report_url_correct(self):
        response = self.client.get(reverse("comment_report"))
        self.assertEqual(response.status_code, 200)

    def test_follower_report_url(self):
        response = self.client.get(reverse("follower_report"))
        self.assertEqual(response.status_code, 200)

    def test_followee_report_url(self):
        response = self.client.get(reverse("followed_report"))
        self.assertEqual(response.status_code, 200)

    def test_ubfollow_url_correct(self):
        response = self.client.get(reverse("un_follow", args=[self.follow.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/followed/report/")
