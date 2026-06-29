from django.db.models import Count, Q, Prefetch
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.groups.models import GroupMember, InterestGroup
from apps.groups.serializers import (
    GroupCreateSerializer,
    GroupDetailSerializer,
    GroupListSerializer,
    GroupMemberSerializer,
    GroupUpdateSerializer,
)
from apps.common.utils import api_response
from apps.feed.models import Post
from apps.feed.serializers import PostSerializer


class GroupListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        base_qs = InterestGroup.objects.annotate(member_count=Count('members'))
        if request.user.is_authenticated:
            groups = base_qs.filter(
                Q(is_public=True) | Q(members__user=request.user)
            ).distinct().order_by("-created_at")
        else:
            groups = base_qs.filter(
                is_public=True
            ).order_by("-created_at")
        serializer = GroupListSerializer(groups, many=True, context={"request": request})
        return api_response(data=serializer.data)


class GroupCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save(creator=request.user)
        GroupMember.objects.create(group=group, user=request.user, role="admin")
        return api_response(
            data=GroupListSerializer(group, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class GroupDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            group = InterestGroup.objects.select_related('creator').prefetch_related(
                Prefetch('members', queryset=GroupMember.objects.select_related('user'))
            ).get(pk=pk)
        except InterestGroup.DoesNotExist:
            return api_response(code=40004, message="小组不存在", status=status.HTTP_404_NOT_FOUND)

        if not group.is_public and not group.members.filter(user=request.user).exists():
            return api_response(code=40003, message="无权查看该小组", status=status.HTTP_403_FORBIDDEN)

        serializer = GroupDetailSerializer(group, context={"request": request})
        return api_response(data=serializer.data)


class GroupUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            group = InterestGroup.objects.get(pk=pk)
        except InterestGroup.DoesNotExist:
            return api_response(code=40004, message="小组不存在", status=status.HTTP_404_NOT_FOUND)

        membership = GroupMember.objects.filter(group=group, user=request.user).first()
        if not membership or membership.role != "admin":
            return api_response(code=40003, message="无权修改小组信息", status=status.HTTP_403_FORBIDDEN)

        serializer = GroupUpdateSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(data=GroupDetailSerializer(group, context={"request": request}).data)


class GroupJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = InterestGroup.objects.get(pk=pk)
        except InterestGroup.DoesNotExist:
            return api_response(code=40004, message="小组不存在", status=status.HTTP_404_NOT_FOUND)

        if GroupMember.objects.filter(group=group, user=request.user).exists():
            return api_response(code=40001, message="已经是小组成员", status=status.HTTP_400_BAD_REQUEST)

        if not group.is_public:
            return api_response(code=40003, message="非公开小组暂不支持直接加入", status=status.HTTP_403_FORBIDDEN)

        GroupMember.objects.create(group=group, user=request.user)
        return api_response(message="加入成功")


class GroupLeaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = InterestGroup.objects.get(pk=pk)
        except InterestGroup.DoesNotExist:
            return api_response(code=40004, message="小组不存在", status=status.HTTP_404_NOT_FOUND)

        membership = GroupMember.objects.filter(group=group, user=request.user).first()
        if not membership:
            return api_response(code=40001, message="不是小组成员", status=status.HTTP_400_BAD_REQUEST)

        if membership.user == group.creator:
            return api_response(code=40003, message="群主不能退出小组", status=status.HTTP_403_FORBIDDEN)

        membership.delete()
        return api_response(message="已退出小组")


class GroupMemberManageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, user_id):
        try:
            group = InterestGroup.objects.get(pk=pk)
        except InterestGroup.DoesNotExist:
            return api_response(code=40004, message="小组不存在", status=status.HTTP_404_NOT_FOUND)

        membership = GroupMember.objects.filter(group=group, user=request.user).first()
        if not membership or membership.role != "admin":
            return api_response(code=40003, message="无权管理成员", status=status.HTTP_403_FORBIDDEN)

        action = request.data.get("action")
        if action not in ("remove", "promote_admin", "demote_admin"):
            return api_response(code=40001, message="无效操作", status=status.HTTP_400_BAD_REQUEST)

        target = GroupMember.objects.filter(group=group, user_id=user_id).first()
        if not target:
            return api_response(code=40004, message="目标用户不是小组成员", status=status.HTTP_404_NOT_FOUND)

        if target.user == group.creator:
            return api_response(code=40003, message="无法操作群主", status=status.HTTP_403_FORBIDDEN)

        if action == "remove":
            target.delete()
            return api_response(message="已移除成员")

        if action == "promote_admin":
            target.role = "admin"
            target.save()
            return api_response(message="已设为管理员")

        if action == "demote_admin":
            target.role = "member"
            target.save()
            return api_response(message="已取消管理员")

        return api_response(code=40001, message="无效操作", status=status.HTTP_400_BAD_REQUEST)


class GroupPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            group = InterestGroup.objects.get(pk=pk)
        except InterestGroup.DoesNotExist:
            return api_response(code=40004, message="小组不存在", status=status.HTTP_404_NOT_FOUND)

        if not group.members.filter(user_id=request.user.id).exists():
            return api_response(code=40003, message="仅成员可查看组内动态", status=status.HTTP_403_FORBIDDEN)

        posts = Post.objects.filter(group_id=pk).order_by("-created_at")

        page = int(request.query_params.get("page", 1))
        page_size = 20
        start = (page - 1) * page_size
        end = start + page_size
        total = posts.count()
        page_posts = posts[start:end]

        serializer = PostSerializer(page_posts, many=True, context={"request": request})
        return api_response(data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": serializer.data,
        })
