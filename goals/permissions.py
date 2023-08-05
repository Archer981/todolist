from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.request import Request

from goals.models import BoardParticipant, Board, GoalCategory, Goal, GoalComment


class BoardPermission(IsAuthenticated):
    """
    Разрешения для доски
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Board) -> bool:
        _filters = {'user': request.user, 'board': obj}
        if request.method not in SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermission(IsAuthenticated):
    """
    Разрешения для категорий
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalCategory) -> bool:
        _filters = {'user': request.user, 'board': obj.board}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermission(IsAuthenticated):
    """
    Разрешения для целей
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Goal) -> bool:
        _filters = {'user': request.user, 'board': obj.category.board}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCommentPermission(IsAuthenticated):
    """
    Разрешения для комментариев
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalComment) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user
