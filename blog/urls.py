from django.urls import path
from .views import (
    CreatePostView,
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    NotificationPostView,
)

urlpatterns = [
    path("post/create/", CreatePostView.as_view(), name="post-create"),
    path("", PostListView.as_view(), name="home"),
    path("post/detail/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/update/<int:pk>/", PostUpdateView.as_view(), name="post-update"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "post/notification/", NotificationPostView.as_view(), name="post-notification"
    ),
]
