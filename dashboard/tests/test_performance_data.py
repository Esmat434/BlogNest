from django.test import TestCase, Client
from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext
from accounts.models import CustomUser
from blog.models import Post, Follow, Comment


class DashboardPerformanceDataTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="12345",
            phone_number="+93141560003",
        )
        self.user2 = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="123456",
            phone_number="+93991210004",
        )

        self.client.login(username="testuser", password="12345")

        self.post = Post.objects.create(
            author=self.user1, title="test title", content="test content"
        )
        self.follow = Follow.objects.create(follower=self.user1, followee=self.user2)

    def test_report_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("report"))

        print(f"ReportView Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 7)

    def test_post_list_report_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("post_list_report"))

        print(f"PostList View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 6)

    def test_post_detail_report_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(
                reverse("post_detail_report", args=[self.post.pk])
            )

        print(f"PostDetail View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 9)

    def test_media_library_report_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("media_library_report"))
        print(f"MediaLibrary View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 5)

    def test_comment_report_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("comment_report"))

        print(f"Comment View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 7)

    def test_follower_report_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("follower_report"))

        print(f"Follower View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 6)

    def test_followed_report_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("followed_report"))

        print(f"Followed View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 6)

    def test_unfollowed_performance_data_check(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("un_follow", args=[self.follow.pk]))

        print(f"UN_Followed View Total Queries: {len(queries)}")
        self.assertLessEqual(len(queries), 7)
