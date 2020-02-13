from django.urls import path

from .views import (
    UserListCreateAPIView,
    UserDetailAPIView,
    TaskListCreateAPIView,
    TaskDetailAPIView,
    SubtaskCreateAPIView,
    SubtaskDetailAPIView,
    CommentCreateAPIView,
    CommentDetailAPIView,
    TagListAPIView,
    TagDetailAPIView
)

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),

    path('subtasks/', SubtaskCreateAPIView.as_view(), name='subtask-create'),
    path('subtasks/<int:pk>/', SubtaskDetailAPIView.as_view(), name='subtask-detail'),

    path('comments/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),

    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetailAPIView.as_view(), name='tag-detail')
]
