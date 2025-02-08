from django.urls import path
from .views import (
    ReportView,
    PostListReportView,
    PostDetailReportView,
    CommentReportView,
    FollowerReportView,
    FollowedReportView,
    UnFollowedView,
    MediaLibraryReportView,
)

urlpatterns = [
    path("dashboard/", ReportView.as_view(), name="dashboard"),
    path("post/list/report/", PostListReportView.as_view(), name="post_list_report"),
    path(
        "post/detail/report/<int:pk>/",
        PostDetailReportView.as_view(),
        name="post_detail_report",
    ),
    path("post/media/", MediaLibraryReportView.as_view(), name="media_library_report"),
    path("comment/report/", CommentReportView.as_view(), name="comment_report"),
    path("follower/report/", FollowerReportView.as_view(), name="follower_report"),
    path("followed/report/", FollowedReportView.as_view(), name="followed_report"),
    path("unfollow/<int:pk>/", UnFollowedView.as_view(), name="un_follow"),
]
