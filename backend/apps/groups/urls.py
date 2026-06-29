from django.urls import path
from apps.groups.views import (
    GroupListView,
    GroupCreateView,
    GroupDetailView,
    GroupUpdateView,
    GroupJoinView,
    GroupLeaveView,
    GroupMemberManageView,
    GroupPostsView,
)

urlpatterns = [
    path("", GroupListView.as_view(), name="group-list"),
    path("create/", GroupCreateView.as_view(), name="group-create"),
    path("<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("<int:pk>/update/", GroupUpdateView.as_view(), name="group-update"),
    path("<int:pk>/join/", GroupJoinView.as_view(), name="group-join"),
    path("<int:pk>/leave/", GroupLeaveView.as_view(), name="group-leave"),
    path("<int:pk>/members/<int:user_id>/", GroupMemberManageView.as_view(), name="group-member-manage"),
    path("<int:pk>/posts/", GroupPostsView.as_view(), name="group-posts"),
]
