from django.test import TestCase, Client
from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext
from accounts.models import CustomUser
from blog.models import Post, PostImage, PostVideo, PostYoutubeVideo, Comment, Follow


class BlogPerformanceDataTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="123",
            phone_number="+93661390907",
        )
        self.client.login(username="test", password="123")
        self.post = Post.objects.create(
            author=self.user, title="test title", content="test content"
        )

    # test_get is get method
    def test_get_post_list_view_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("home"))
        print(f"Total of queries from PostList view: {len(queries)}")
        self.assertLessEqual(len(queries), 8)

    # test_post is post method
    def test_post_post_list_view_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.post(
                reverse("home"), data={"filter_option": "viewer"}
            )
        print(f"Total of queries from PostList view: {len(queries)}")
        self.assertLessEqual(len(queries), 8)

    def test_get_post_detail_view_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("post-detail", args=[self.post.pk]))
        print(f"Total of queries from PostDetail view: {len(queries)}")
        self.assertLessEqual(len(queries), 17)

    def test_post_post_detail_view_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.post(
                reverse("post-detail", args=[self.post.pk]), data={"btn": "like"}
            )
        print(f"total of queries from PostDetail view: {len(queries)}")
        self.assertLessEqual(len(queries), 18)

    def test_get_post_update_view_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("post-update", args=[self.post.pk]))
        print(f"total of queries from PostUpadet view: {len(queries)}")
        self.assertLessEqual(len(queries), 9)

    def test_post_post_upadte_view_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.post(reverse("post-update", args=[self.post.pk]))
        print(f"total of queries from PostUpdate view: {len(queries)}")
        self.assertLessEqual(len(queries), 6)

    def test_get_post_delete_view_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("post-delete", args=[self.post.pk]))
        print(f"total of queries from PostDelete view: {len(queries)}")
        self.assertLessEqual(len(queries), 18)

    def test_get_notification_post_view_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("post-notification"))
        print(f"total of quries from NotificationPost view: {len(queries)}")
        self.assertLessEqual(len(queries), 20)
