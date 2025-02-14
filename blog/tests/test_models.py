from django.test import TestCase, Client
from accounts.models import CustomUser
from blog.models import Post, PostImage, PostVideo, PostYoutubeVideo, Comment, Follow


class BlogModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="1234",
            phone_number="+93554420090",
        )
        self.user1 = CustomUser.objects.create_user(
            username="test1",
            email="test1@gmail.com",
            password="12345",
            phone_number="+93512464390",
        )

        self.post = Post.objects.create(
            author=self.user, title="title test", content="title content"
        )
        self.image = PostImage.objects.create(post=self.post, image="test.jpg")
        self.video = PostVideo.objects.create(post=self.post, video="test.mp4")
        self.youtube = PostYoutubeVideo.objects.create(
            post=self.post, video_url="www.youtube.com"
        )
        self.commment = Comment.objects.create(
            post=self.post, user=self.user, content="test comment"
        )
        self.follow = Follow.objects.create(follower=self.user, followee=self.user1)

    def test_customuser_model_correct(self):
        self.assertEqual(self.user.username, "test")

    def test_post_model_correct(self):
        self.assertEqual(self.post.title, "title test")

    def test_post_image_model_correct(self):
        self.assertEqual(self.image.image, "test.jpg")

    def test_post_video_mode_correct(self):
        self.assertEqual(self.video.video, "test.mp4")

    def test_post_youtube_video_model_correct(self):
        self.assertEqual(self.youtube.video_url, "www.youtube.com")

    def test_comment_model_correct(self):
        self.assertEqual(self.commment.content, "test comment")

    def test_follow_model_correct(self):
        self.assertEqual(self.follow.follower, self.user)
