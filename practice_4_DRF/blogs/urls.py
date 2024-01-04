from django.urls import path
from .views import (
    BlogListCreateView,
    BlogDetailView,
    CommentListCreateView,
    CommentDetailView,
    CommentReplyListCreateView,
    CommentReplyDetailView,
    UpvoteCreateView,
    UpvoteDetailView,
    CommentUpvoteCreateView,
    CommentUpvoteDetailView,
    CommentReplyUpvoteCreateView,
    CommentReplyUpvoteDetailView,
)

urlpatterns = [
    path("blogs/", BlogListCreateView.as_view(), name="blog-list-create"),
    path("blogs/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
    path("blogs/<slug:slug>/upvote/", UpvoteCreateView.as_view(), name="blog-upvote"),
    path(
        "blogs/<slug:slug>/upvote/<int:pk>/",
        UpvoteDetailView.as_view(),
        name="blog-upvote-delete",
    ),
    path("comment/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("comment/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
    path(
        "comment-upvote/",
        CommentUpvoteCreateView.as_view(),
        name="comment-upvote-create",
    ),
    path(
        "comment-upvote/<int:pk>/",
        CommentUpvoteDetailView.as_view(),
        name="comment-upvote-delete",
    ),
    path(
        "replies/",
        CommentReplyListCreateView.as_view(),
        name="comment-reply-list-create",
    ),
    path(
        "replies/<int:pk>/",
        CommentReplyDetailView.as_view(),
        name="comment-reply-detail",
    ),
    path(
        "reply-upvote/",
        CommentReplyUpvoteCreateView.as_view(),
        name="reply-upvote-create",
    ),
    path(
        "reply-upvote/<int:pk>/",
        CommentReplyUpvoteDetailView.as_view(),
        name="reply-upvote-create",
    ),
]
