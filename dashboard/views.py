import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views import View
from django.db.models import Count, Sum, Prefetch, Q
from django.db.models.functions import ExtractMonth, ExtractYear
from blog.models import Post, Follow, PostVideo
from .mixins import LoginRequiredMixin
from .loggers import logger


class ReportView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User {request.user.username} requested from report to post and follow from app /dashboard/views/ReportView."
        )

        context = self.get_post_report(request)

        logger.debug(
            f"{context['posts'].count()} and total_follower {context['total_follower']} ans total_followed {context['total_followed']} posts retrieved successfully for user {request.user.username} from app /dashboard/views/ReportView."
        )

        return render(request, "Dashboard/dashboard.html", context=context)

    def get_post_report(self, request):
        posts = Post.objects.filter(author=request.user).annotate(
            total_comments=Count("Comment") or 0
        )
        monthly_posts_data = self.get_monthly_post_data(request.user)

        totals = Follow.objects.aggregate(
            total_follower=Count("id", filter=Q(followee=request.user)),
            total_followed=Count("id", filter=Q(follower=request.user)),
        )

        context = {
            "posts": posts,
            "monthly_posts_data": monthly_posts_data,
            "total_follower": totals["total_follower"],
            "total_followed": totals["total_followed"],
        }
        return context

    def get_monthly_post_data(self, user):
        current_year = datetime.now().year
        monthly_data = (
            Post.objects.filter(author=user, created_time__year=current_year)
            .annotate(month=ExtractMonth("created_time"))
            .values("month")
            .annotate(
                total_posts=Count("id"),
                total_likes=Sum("likes"),
                total_views=Sum("views"),
                total_comments=Count("Comment"),
            )
            .order_by("month")
        )

        monthly_results = [
            {
                "total_posts": 0,
                "total_likes": 0,
                "total_views": 0,
                "total_comments": 0,
            }
        ]
        if monthly_data:
            monthly_results = []
            for data in monthly_data:
                monthly_results.append(
                    {
                        "total_posts": data["total_posts"],
                        "total_likes": data["total_likes"] or 0,
                        "total_views": data["total_views"] or 0,
                        "total_comments": data["total_comments"] or 0,
                    }
                )
        return json.dumps(monthly_results)


class PostListReportView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User {request.user.username} requested from post list report to post from app /dashboard/views/PostListReportView."
        )
        posts = self.get_post(request)

        if not posts:
            logger.warning(
                f"User {request.user.username} Not Found Post from app /dashboard/views/PostListReportView."
            )

        logger.debug(
            f"{posts.count()} posts retrieved successfully for user {request.user.username} from app /dashboard/views/PostListReportView."
        )
        return render(request, "Dashboard/PostListReport.html", {"posts": posts})

    def get_post(self, request):
        posts = Post.objects.filter(author=request.user).order_by("-created_time")
        return posts


class PostDetailReportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        logger.info(
            f"User {request.user.username} requested post detail report for post ID: {pk} from app /dashboard/views/PostDetailReportView."
        )

        post = self.get_post(request, pk)
        if not post:
            logger.warning(
                f"Post ID {pk} not found for user {request.user.username} from app /dashboard/views/PostDetailReportView."
            )
            return HttpResponseNotFound("Page Not Found")
        logger.debug(
            f"Post details report retrieved successfully for post ID: {pk} from app /dashboard/views/PostDetailReportView."
        )
        return render(request, "Dashboard/PostDetailReport.html", {"post": post})

    def get_post(self, request, pk):
        try:
            post = (
                Post.objects.select_related("author")
                .prefetch_related(
                    Prefetch("image"), Prefetch("video"), Prefetch("youtube_video")
                )
                .get(id=pk, author=request.user)
            )
        except Post.DoesNotExist:
            return None
        return post


class MediaLibraryReportView(LoginRequiredMixin, View):
    def get(self, request):
        media_files = PostVideo.objects.filter(post__author=request.user)
        return render(
            request, "Dashboard/mediaLibraryReport.html", {"media_files": media_files}
        )


class CommentReportView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User {request.user.username} requested from comment report to post for get comment from app /dashboard/views/CommentReportView."
        )
        posts = self.get_comment(request)

        logger.debug(
            f"comment report retrived successfully from app /dashboard/views/CommentReportView."
        )
        return render(request, "Dashboard/CommentReport.html", {"posts": posts})

    def get_comment(self, request):
        posts = Post.objects.filter(author=request.user).prefetch_related(
            Prefetch("Comment")
        )
        return posts


# this class shows every person that followed yourself
class FollowerReportView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User {request.user.username} requested from app /dashboard/views/FollowerReportView."
        )
        followers = Follow.objects.filter(followee=request.user)
        if not followers:
            logger.warning(
                f"User {request.user.username} Not Found Follower from app /dashboard/views/FollowerReportView."
            )

        logger.debug(
            f"Follower Report for user {request.user.username} retrieved. Total followers: {followers.count()} from app /dashboard/views/FollowerReportView."
        )
        return render(
            request, "Dashboard/FollowerReport.html", {"followers": followers}
        )


# this class shows every person that you follow
class FollowedReportView(LoginRequiredMixin, View):
    def get(self, request):
        logger.info(
            f"User {request.user.username} requested from app /dashboard/views/FollowedReportReportView."
        )
        followeds = Follow.objects.filter(follower=request.user)
        if not followeds:
            logger.warning(
                f"User {request.user.username} requested from app /dashboard/views/FollowedReportReportView."
            )

        logger.debug(
            f"Followed Report Retrived Successfuly from app /dashboard/views/FollowedReportReportView."
        )
        return render(
            request, "Dashboard/followedReport.html", {"followeds": followeds}
        )


# this class can unfollow every person that you follow
class UnFollowedView(LoginRequiredMixin, View):
    def get(self, request, pk):
        logger.info(
            f"User {request.user.username} requested from un-followed to ID: {pk} from app /dashboard/views/UNFollowedReportReportView."
        )

        try:
            followed = Follow.objects.get(id=pk)
        except Follow.DoesNotExist:
            logger.warning(
                f"User {request.user.username} Not Found Followed ID: {pk} from app /dashboard/views/UNFollowedReportReportView."
            )
            return HttpResponseNotFound("Follower DoesNotExist!")
        followed.delete()
        logger.debug(
            f"ID: {pk} retrived successfully from {request.user.username} from app /dashboard/views/UNFollowedReportReportView."
        )
        return redirect("/followed/report/")
