from django.urls import path

from goals.apps import GoalsConfig
from goals.views.categories import *
from goals.views.comments import CommentCreateView, CommentListView, CommentDetailView
from goals.views.goals import *

app_name = GoalsConfig.name

urlpatterns = [
    path('goal_category/create', CategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', CategoryListView.as_view(), name='category-list'),
    path('goal_category/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('goal/create', GoalCreateView.as_view(), name='create-goal'),
    path('goal/list', GoalListView.as_view(), name='goal-list'),
    path('goal/<int:pk>', GoalDetailView.as_view(), name='goal-detail'),
    path('goal_comment/create', CommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', CommentListView.as_view(), name='comment-list'),
    path('goal_comment/<int:pk>', CommentDetailView.as_view(), name='comment-detail'),
]
