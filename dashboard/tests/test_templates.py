from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from blog.models import Post


class DashboardTemplateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="12345",
            phone_number="+93771640009",
        )
        self.post = Post.objects.create(
            author=self.user1, title="test title", content="test content"
        )
        self.client.login(username="testuser", password="12345")

    def test_report_template_exists(self):
        response = self.client.get(reverse("report"))
        self.assertTemplateUsed(response, "Dashboard/report.html")

    def test_post_list_report_template_exists(self):
        response = self.client.get(reverse("post_list_report"))
        self.assertTemplateUsed(response, "Dashboard/PostListReport.html")

    def test_post_detail_report_template_exists(self):
        response = self.client.get(reverse("post_detail_report", args=[self.post.pk]))
        self.assertTemplateUsed(response, "Dashboard/PostDetailReport.html")

    def test_media_library_report_template_exists(self):
        response = self.client.get(reverse("media_library_report"))
        self.assertTemplateUsed(response, "Dashboard/mediaLibraryReport.html")

    def test_comment_report_template_exists(self):
        response = self.client.get(reverse("comment_report"))
        self.assertTemplateUsed(response, "Dashboard/CommentReport.html")

    def test_follower_report_templeate_exists(self):
        response = self.client.get(reverse("follower_report"))
        self.assertTemplateUsed(response, "Dashboard/FollowerReport.html")

    def test_followed_report_template_exists(self):
        response = self.client.get(reverse("followed_report"))
        self.assertTemplateUsed(response, "Dashboard/followedReport.html")
