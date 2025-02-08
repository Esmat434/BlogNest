from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from blog.models import Post


class BlogUrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="123",
            phone_number="+93889110020",
        )
        self.client.login(username="test", password="123")

        self.post = Post.objects.create(
            author=self.user, title="test1 title", content="test1 content"
        )

        self.post_filter = Post.objects.filter(author=self.user)

    def test_get_create_post_url_templates_exists(self):
        response = self.client.get(reverse("post-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/createpost.html")

    def test_post_create_post_url_exists(self):
        response = self.client.post(
            reverse("post-create"),
            data={"title": "test title", "content": "test content"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_get_post_list_url_template_context_data_exists(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/home.html")
        self.assertIn("posts", response.context)
        self.assertEqual(list(response.context["posts"]), list(self.post_filter))

    def test_post_post_list_url_template_context_data_exists(self):
        response = self.client.post(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/home.html")
        self.assertIn("posts", response.context)
        self.assertEqual(list(response.context["posts"]), list(self.post_filter))

    def test_get_post_detail_url_template_context_data_exists(self):
        response = self.client.get(reverse("post-detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/postDetail.html")
        self.assertIn("post", response.context)
        self.assertIn("is_like", response.context)
        self.assertIn("is_saved", response.context)
        self.assertIn("is_follow", response.context)
        self.assertEqual(response.context["post"], self.post)
        self.assertFalse(response.context["is_like"])
        self.assertFalse(response.context["is_saved"])
        self.assertFalse(response.context["is_follow"])

    def test_get_post_update_url_template_context_data_exists(self):
        response = self.client.get(reverse("post-update", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/postUpdate.html")
        self.assertIn("post", response.context)
        self.assertEqual(response.context["post"], self.post)

    def test_post_post_update_url_template_context_data_exists(self):
        response = self.client.post(
            reverse("post-update", args=[self.post.pk]),
            data={"btn": "submit", "title": "test title", "content": "test content"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/PostListReport.html")
        self.assertIn("message", response.context)
        self.assertEqual(response.context["message"], "this post successfuly update!")

    def test_post_post_update_delete_image_redirect_url_exists(self):
        response = self.client.post(
            reverse("post-update", args=[self.post.pk]),
            data={
                "btn": "delete_image",
                "title": "test title",
                "content": "test content",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("post-update", args=[self.post.pk]))

    def test_post_post_update_delete_image_redirect_url_exists(self):
        response = self.client.post(
            reverse("post-update", args=[self.post.pk]),
            data={
                "btn": "delete_video",
                "title": "test title",
                "content": "test content",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("post-update", args=[self.post.pk]))

    def test_get_post_delete_redirect_url_exists(self):
        response = self.client.get(reverse("post-delete", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_get_notification_post_url_template_context_data_exists(self):
        response = self.client.get(reverse("post-notification"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/notificationPost.html")
        self.assertIn("posts", response.context)
        self.assertEqual(list(response.context["posts"]), list())
