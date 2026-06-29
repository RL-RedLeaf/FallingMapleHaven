from django.urls import path
from apps.friends.views import (
    FriendRequestView,
    FriendHandleView,
    UnfriendView,
    FriendListView,
    FriendRequestReceivedView,
    UserSearchView,
)

urlpatterns = [
    path("request/", FriendRequestView.as_view(), name="friend-request"),
    path("handle/", FriendHandleView.as_view(), name="friend-handle"),
    path("unfriend/", UnfriendView.as_view(), name="friend-unfriend"),
    path("", FriendListView.as_view(), name="friend-list"),
    path("requests/", FriendRequestReceivedView.as_view(), name="friend-requests"),
    path("search/", UserSearchView.as_view(), name="friend-search"),
]
