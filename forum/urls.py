"""
URLs for forum.
"""

from django.urls import include, path

from forum.views.comments import CommentsAPIView, CreateThreadCommentAPIView
from forum.views.flags import CommentFlagAPIView, ThreadFlagAPIView
from forum.views.pins import PinThreadAPIView, UnpinThreadAPIView
from forum.views.proxy import ForumProxyAPIView
from forum.views.search import SearchThreadsView
from forum.views.votes import CommentVoteView, ThreadVoteView

api_patterns = [
    # thread votes APIs
    path(
        "threads/<str:thread_id>/votes",
        ThreadVoteView.as_view(),
        name="thread-vote",
    ),
    path(
        "comments/<str:comment_id>/votes",
        CommentVoteView.as_view(),
        name="comment-vote",
    ),
    # abuse comment/thread APIs
    path(
        "comments/<str:comment_id>/abuse_<str:action>",
        CommentFlagAPIView.as_view(),
        name="comment-flags-api",
    ),
    path(
        "threads/<str:thread_id>/abuse_<str:action>",
        ThreadFlagAPIView.as_view(),
        name="thread-flags-api",
    ),
    # pin/unpin thread APIs
    path("threads/<str:thread_id>/pin", PinThreadAPIView.as_view(), name="pin-thread"),
    path(
        "threads/<str:thread_id>/unpin",
        UnpinThreadAPIView.as_view(),
        name="unpin-thread",
    ),
    # comments API
    path(
        "comments/<str:comment_id>",
        CommentsAPIView.as_view(),
        name="comments-api",
    ),
    # search threads API
    path(
        "search/threads",
        SearchThreadsView.as_view(),
        name="search-thread-api",
    ),
    path(
        "threads/<str:thread_id>/comments",
        CreateThreadCommentAPIView.as_view(),
        name="create-parent-comment-api",
    ),
    # Proxy view for various API endpoints
    path(
        "<path:suffix>",
        ForumProxyAPIView.as_view(),
        name="forum_proxy",
    ),
]

urlpatterns = [
    path("api/v2/", include(api_patterns)),
]
