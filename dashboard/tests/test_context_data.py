from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from blog.models import Post, Comment, Follow


class DashboardContextDataTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="123456",
            phone_number="+9377151603",
        )
        self.user2 = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="1234567",
            phone_number="+93889920009",
        )

        self.client.login(username="testuser", password="123456")

        self.post = Post.objects.create(
            author=self.user1, title="test title", content="test content"
        )
        Follow.objects.create(follower=self.user1, followee=self.user2)
        Follow.objects.create(follower=self.user2, followee=self.user1)

    def test_report_view_context_data_correct(self):
        response = self.client.get(reverse("report"))

        self.assertIn("posts", response.context)
        self.assertIn("total_follower", response.context)
        self.assertIn("total_followed", response.context)

        self.assertEqual(len(response.context["posts"]), 1)
        self.assertEqual(response.context["total_follower"], 1)
        self.assertEqual(response.context["total_followed"], 1)

    def test_post_list_report_context_data_correct(self):
        response = self.client.get(reverse("post_list_report"))
        self.assertIn("posts", response.context)
        self.assertEqual(len(response.context["posts"]), 1)

    def test_post_detail_report_context_data_correct(self):
        response = self.client.get(reverse("post_detail_report", args=[self.post.pk]))
        self.assertIn("post", response.context)
        self.assertEqual(response.context["post"], self.post)

    def test_media_library_report_context_data_correct(self):
        response = self.client.get(reverse("media_library_report"))
        self.assertIn("media_files", response.context)
        self.assertEqual(len(response.context["media_files"]), 0)

    def test_comment_report_context_data_correct(self):
        response = self.client.get(reverse("comment_report"))
        self.assertIn("posts", response.context)
        self.assertEqual(len(response.context["posts"]), 1)

    def test_folower_report_context_data_correct(self):
        response = self.client.get(reverse("follower_report"))
        self.assertIn("followers", response.context)
        self.assertEqual(len(response.context["followers"]), 1)

    def test_followed_report_context_data_correct(self):
        response = self.client.get(reverse("followed_report"))
        self.assertIn("followeds", response.context)
        self.assertEqual(len(response.context["followeds"]), 1)
