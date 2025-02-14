from datetime import date
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.db.models import Count, Prefetch
from django.views import View
from .models import *
from .advance_post_reommended import rank_posts
from .Cosine_Similarity_Algorithm import get_similar_posts
from .mixins import LoginRequiredMixin, OwnerRequiredMixin
from .loggers import logger


# Add LoginRequired ModelMixin
class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(f"User: {request.user.username} requested send successfully.")
        return render(request, "blog/createpost.html")

    def post(self, request):
        logger.info(
            f"User: {request.user.username} will post data to create post from app /blog/view/CreatePostView."
        )
        data = request.POST
        title = data.get("title")
        content = data.get("content")
        images = request.FILES.getlist("images")
        videos = request.FILES.getlist("videos")
        youtube_video_url = data.get("video_url")
        status = data.get("status")
        post = Post.objects.create(
            author=request.user, title=title, content=content, status=status
        )

        if youtube_video_url:
            video_url = self.convert_to_embed_url(youtube_video_url)
            if video_url:
                PostYoutubeVideo.objects.create(post=post, video_url=video_url)

        for image in images:
            PostImage.objects.create(post=post, image=image)

        for video in videos:
            PostVideo.objects.create(post=post, video=video)

        logger.debug(
            f"User: {request.user.username} create post successfully from app /blog/view/CreatePostView."
        )
        return redirect(reverse("post_list_report"))

    def convert_to_embed_url(self, youtube_url):
        if "youtube.be" in youtube_url:
            video_id = youtube_url.split("/")[-1]
        elif "youtube.com/watch" in youtube_url:
            video_id = youtube_url.split("v=")[1].split("&")[0]
        else:
            return None
        return f"https://www.youtube.com/embed/{video_id}"


class PostListView(View):
    def get(self, request):
        logger.info(
            f"User: {request.user.username} request sended for show posts successfully from app /blog/view/PostListView."
        )
        posts = rank_posts()
        return render(request, "blog/home.html", {"posts": posts})

    def post(self, request):
        logger.info(
            f"User: {request.user.username} order by post with like or follow or created_time successfully from app /blog/view/PostListView."
        )
        btn = request.POST.get("btn")
        if btn == "search-button":
            posts = self.search_data(request)
            return render(request, "blog/home.html", {"posts": posts})
        posts = self.check_post_filterization(request)
        return render(request, "blog/home.html", {"posts": posts})

    def check_post_filterization(self, request):
        data = request.POST
        filter_option_post = data.get("filter_option")
        queryset = Post.objects.filter(status="published").annotate(
            comment_count=Count("Comment")
        )

        if filter_option_post == "viewer":
            return queryset.order_by("-views")
        elif filter_option_post == "popular":
            return queryset.order_by("-likes")
        elif filter_option_post == "new":
            return queryset.order_by("-created_time")
        else:
            return queryset.order_by("-created_time")

    def search_data(self, request):
        query_name = request.POST.get("search-input")
        if query_name:
            posts_as_title = Post.objects.filter(
                title__icontains=query_name, status="published"
            )
            posts_as_content = Post.objects.filter(
                content__icontains=query_name, status="published"
            )
            posts = posts_as_content | posts_as_title
            return posts
        return rank_posts()


# Add LoginRequirement ModelMixin
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        logger.info(
            f"User: {request.user.username} sended request to hsow detail of post successfully from app /blog/view/PostDetailView."
        )
        post = self.get_post(pk)
        if post:
            post.views.add(request.user)
            like_status, post_save_status, follow_status = (
                self.check_like_and_saved_and_follow_status(request, post)
            )
            similar_posts = get_similar_posts(pk)
            return render(
                request,
                "blog/postDetail.html",
                {
                    "post": post,
                    "similar_posts": similar_posts,
                    "is_like": like_status,
                    "is_saved": post_save_status,
                    "is_follow": follow_status,
                },
            )
        logger.warning(
            f"User: {request.user.useranme} send request but post does not exists from app /blog/view/PostDeatilView."
        )
        return HttpResponseNotFound("Page not found")

    def post(self, request, pk):
        logger.info(
            f"User: {request.user.username} send requeste successfully to create like or folloe or comment or saved or delete something from app /blog/view/PostDetailView."
        )
        data = request.POST
        btn = data.get("btn")
        post = self.get_post(pk)
        like_status, post_saved_status, follow_status = (
            self.check_like_and_saved_and_follow_status(request, post)
        )
        similar_posts = get_similar_posts(pk)
        if btn == "like":
            like_status = self.get_like(request, post)
        elif btn == "saved":
            post_saved_status = self.check_post_saved(request, post)
        elif btn == "follow":
            follow_status = self.get_followed(request, post)
        elif btn == "comment":
            self.add_comment(request, post)
        elif btn == "delete_comment":
            self.delete_comment(request)
        elif btn == "reply":
            self.add_reply_of_comment(request, post)
        logger.debug(
            f"User: {request.user.username} created successfully like or comment or follow or delete something from app /blog/view/PostdetailView."
        )
        return render(
            request,
            "blog/postDetail.html",
            {
                "post": post,
                "similar_posts": similar_posts,
                "is_like": like_status,
                "is_saved": post_saved_status,
                "is_follow": follow_status,
            },
        )

    def get_post(self, pk):
        try:
            post = Post.objects.prefetch_related(
                Prefetch("image"),
                Prefetch("video"),
                Prefetch("youtube_video"),
                Prefetch("Comment"),
            ).get(id=pk, status="published")
            return post
        except Post.DoesNotExist:
            return None

    def add_comment(self, request, post):
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)

    def delete_comment(self, request):
        data = request.POST
        delete_comment_id = data.get("delete_comment_id")
        try:
            delete_comment = Comment.objects.get(id=delete_comment_id)
            delete_comment.delete()
        except Comment.DoesNotExist:
            logger.warning(
                f"User: {request.user.username} requested faild comment does not exists to delete from app /blog/view/PostDetailView."
            )
            return HttpResponse("Comment not found", status=404)

    def add_reply_of_comment(self, request, post):
        data = request.POST
        comment_id = data.get("comment_id")
        reply_content = data.get("reply_content")

        try:
            comment = Comment.objects.get(id=comment_id)
            Comment.objects.create(
                post=post, user=request.user, parents=comment, content=reply_content
            )
        except Comment.DoesNotExist:
            logger.warning(
                f"User: {request.user.username} requested faild comment does not exists to reply from app /blog/view/PostDetailView."
            )
            return HttpResponse("Comment not found", status=404)

    def get_like(self, request, post):
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return None
        post.likes.add(request.user)
        return True

    def check_post_saved(self, request, post):
        if post.saved.filter(id=request.user.id).exists():
            post.saved.remove(request.user)
            return None
        post.saved.add(request.user)
        return True

    def get_followed(self, request, post):
        queryset = Follow.objects.filter(follower=request.user, followee=post.author)
        if queryset.exists():
            queryset.delete()
            return False
        Follow.objects.create(follower=request.user, followee=post.author)
        return True

    def check_like_and_saved_and_follow_status(self, request, post):
        like_status = post.likes.filter(id=request.user.id).exists()
        post_save_status = post.saved.filter(id=request.user.id).exists()
        follow_status = Follow.objects.filter(
            follower=request.user, followee=post.author
        ).exists()
        return (like_status, post_save_status, follow_status)


class PostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, View):
    def get(self, request, pk):
        logger.info(
            f"User: {request.user.username} send request to update post from app /blog/view/PostUpdateView."
        )
        try:
            post = Post.objects.prefetch_related(
                Prefetch("image"), Prefetch("video"), Prefetch("youtube_video")
            ).get(id=pk)
        except Post.DoesNotExist:
            logger.warning(
                f"User: {request.user.username} requested faild post does not exists from app /blog/view/PostUpdateView."
            )
            return HttpResponse("404 page not found!")
        logger.debug(
            f"User: {request.user.username} post successfully updated from app /blog/view/PostUpdateView"
        )
        return render(request, "blog/postUpdate.html", {"post": post})

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return HttpResponse("404 page not found!")
        data = request.POST
        btn = data.get("btn")
        if btn == "submit":
            self.submit_changes(request, post)
            return redirect(reverse("post_list_report"))
        elif btn == "delete_image":
            self.delete_image(request)
            return redirect(reverse("post-update", args=[pk]))
        elif btn == "delete_video":
            self.delete_video(request)
            return redirect(reverse("post-update", args=[pk]))
        return redirect(reverse("post_list_report"))

    def submit_changes(self, request, post):
        data = request.POST
        title = data.get("title")
        content = data.get("content")
        status = data.get("status")
        images = request.FILES.getlist("images")
        videos = request.FILES.getlist("videos")
        youtube_url = data.get("youtube_url")
        youtube_video_url = self.convert_to_embed_url(youtube_url)
        if youtube_video_url:
            PostYoutubeVideo.objects.create(post=post, video_url=youtube_video_url)

        if images:
            for image in images:
                PostImage.objects.create(post=post, image=image)

        if videos:
            for video in videos:
                PostVideo.objects.create(post=post, video=video)

        post.title = title
        post.content = content
        post.status = status
        post.save()

    def delete_image(self, request):
        image_id = request.POST.get("image_id")
        PostImage.objects.filter(id=image_id).delete()

    def delete_video(self, request):
        video_id = request.POST.get("video_id")
        PostVideo.objects.filter(id=video_id).delete()

    def convert_to_embed_url(self, youtube_url):
        if youtube_url:
            if "youtube.be" in youtube_url:
                video_id = youtube_url.split("/")[-1]
            elif "youtube.com/watch" in youtube_url:
                video_id = youtube_url.split("v=")[1].split("&")[0]
            else:
                return None
            return f"https://www.youtube.com/embed/{video_id}"
        return None


class PostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, View):
    def get(self, request, pk):
        logger.info(
            f"User: {request.user.username} send request to delete post from app /blog/view/PostDeleteView."
        )
        post = get_object_or_404(Post, id=pk)
        post.delete()
        return redirect(reverse('post_list_report'))


class NotificationPostView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User: {request.user.username} send request to see their notification from app /blog/view/NotificationPostView."
        )
        today = date.today()
        followees = Follow.objects.filter(follower=request.user).values_list(
            "followee", flat=True
        )
        posts = (
            Post.objects.filter(
                author__in=followees, status="published", created_time__date=today
            )
            .select_related("author")
            .annotate(comment_count=Count("Comment"))
            .order_by("-created_time")
        )
        return render(request, "blog/notificationPost.html", {"posts": posts})
