from django.urls import path
from apps.feed.views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostDeleteView,
    LikeView,
    CommentListView,
    CommentCreateView,
    CommentDeleteView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<int:pk>/like/", LikeView.as_view(), name="post-like"),
    path("<int:pk>/comments/", CommentListView.as_view(), name="comment-list"),
    path("<int:pk>/comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
]
