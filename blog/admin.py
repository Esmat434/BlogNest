from django.contrib import admin
from .models import Post, PostImage, PostVideo, PostYoutubeVideo, Comment, Follow

# Register your models here.


class PosImageAdmin(admin.StackedInline):
    model = PostImage
    fields = ["image"]
    extra = 0


class PostVideoAdmin(admin.StackedInline):
    model = PostVideo
    fields = ["video"]
    extra = 0


class PostYoutubeVideoAdmin(admin.StackedInline):
    model = PostYoutubeVideo
    fields = ["video_url"]
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "title", "status", "slug", "created_time"]
    inlines = [PosImageAdmin, PostVideoAdmin, PostYoutubeVideoAdmin]
    list_filter = ["title"]
    search_fields = ["authore,title"]
    ordering = ["title"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "parents", "created_time"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["id", "follower", "followee"]
    list_filter = ["follower", "followee"]
    search_fields = ["follower", "followee"]
