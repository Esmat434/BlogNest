from datetime import datetime
from django.db import models
from accounts.models import CustomUser
from django.utils.text import slugify
from datetime import datetime

# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = [("published", "published"), ("draft", "draft")]
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Author"
    )
    title = models.CharField(max_length=200, verbose_name="title")
    content = models.TextField(verbose_name="content")
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="published"
    )
    slug = models.SlugField(unique=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name="like_post", blank=True)
    views = models.ManyToManyField(CustomUser, related_name="view_post", blank=True)
    saved = models.ManyToManyField(CustomUser, related_name="saved_post", blank=True)
    shared_count = models.PositiveBigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def total_like(self):
        return self.likes.count()

    def total_view(self):
        return self.views.count()

    def __str__(self):
        return self.title

    def get_features(self):
        # استخراج ویژگی‌ها
        created_time_naive = self.created_time.replace(
            tzinfo=None
        )  # تبدیل تاریخ به نوع naive
        days_diff = (datetime.now() - created_time_naive).days
        content_length = len(self.content.split())
        features = [self.likes.count(), self.views.count(), content_length, days_diff]
        return features


def post_image_upload_path(instance, filename):
    return f"images/post_image/{instance.post.author.username}/{filename}"


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to=post_image_upload_path, blank=True)

    def __str__(self):
        return f"image for {self.post.title}"


def post_video_upload_path(instance, filename):
    return f"files/post_video/{instance.post.author.username}/{filename}"


class PostVideo(models.Model):
    def get_current_month():
        return datetime.now().date()

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="video")
    video = models.FileField(upload_to=post_video_upload_path, blank=True)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=100, default="")
    created_time = models.DateField(default=get_current_month)

    def save(self, *args, **kwargs):
        if not self.file_type:
            self.file_type = self.get_file_type()
        if not self.size:
            self.size = self.get_file_size()
        return super().save(*args, **kwargs)

    def get_file_type(self):
        if self.video.name.endswith(".jpeg"):
            return "JPEG"
        elif self.video.name.endswith(".gif"):
            return "GIF"
        elif self.video.name.endswith(".webp"):
            return "WEBP"
        elif self.video.name.endswith(".svg+xml"):
            return "SVG+XML"
        elif self.video.name.endswith(".bmp"):
            return "BMP"
        elif self.video.name.endswith(".tiff"):
            return "TIFF"
        elif self.video.name.endswith(".mp4"):
            return "MP4"
        elif self.video.name.endswith(".webm"):
            return "WEBM"
        elif self.video.name.endswith(".x-msvideo"):
            return "X-MSVIDEO"
        elif self.video.name.endswith(".quicktime"):
            return "QUICKTIME"
        elif self.video.name.endswith(".x-matroska"):
            return "X-MATROSKA"
        elif self.video.name.endswith(".x-ms-wmv"):
            return "X-MS-WMV"
        elif self.video.name.endswith(".mpeg"):
            return "MPEG"
        elif self.video.name.endswith(".wav"):
            return "WAV"
        elif self.video.name.endswith(".acc"):
            return "ACC"
        elif self.video.name.endswith(".pdf"):
            return "PDF"
        elif self.video.name.endswith(".zip"):
            return "ZIP"
        else:
            return None

    def get_file_size(self):
        if self.video:
            file_size = self.video.size
            if file_size < 1024:
                return f"{file_size} B"
            elif file_size < 1024 * 1024:
                return f"{file_size / 1024:.2f} KB"
            else:
                return f"{file_size / (1024 * 1024):.2f} MB"

    def __str__(self):
        return f"video for {self.post.title}"


class PostYoutubeVideo(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="youtube_video"
    )
    video_url = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Comment")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    parents = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    content = models.TextField(verbose_name="content")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="following"
    )
    followee = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="followers"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followee")

    def __str__(self):
        return f"{self.follower.username} follows {self.followee.username}"
