from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from goals.permissions import GoalCommentPermission
from goals.serializers import *


class CommentCreateView(generics.CreateAPIView):
    """
    Вьюшка создания комментария
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer


class CommentListView(generics.ListAPIView):
    """
    Вьюшка просмотра списка комментариев
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentWithUserSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Вьюшка просмотра одного комментария
    """
    permission_classes = [GoalCommentPermission]
    serializer_class = GoalCommentWithUserSerializer
    queryset = GoalComment.objects.select_related('user')

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.select_related('user').filter(
            goal__category__board__participants__user=self.request.user
        )

