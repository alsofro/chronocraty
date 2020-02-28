from django.urls import path

from .views import (
    UserListCreateAPIView,
    UserDetailAPIView,
    TaskListCreateAPIView,
    TaskDetailAPIView,
    SubtaskListCreateAPIView,
    SubtaskDetailAPIView,
    CommentListCreateAPIView,
    CommentDetailAPIView,
    TagListCreateAPIView,
    TagDetailAPIView
)

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),

    path('tasks/<int:task_pk>/subtasks/', SubtaskListCreateAPIView.as_view(), name='subtask-create'),
    path('tasks/<int:task_pk>/subtasks/<int:pk>/', SubtaskDetailAPIView.as_view(), name='subtask-detail'),

    path('tasks/<int:task_pk>/comments/', CommentListCreateAPIView.as_view(), name='comment-create'),
    path('tasks/<int:task_pk>/comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),

    path('tasks/<int:task_pk>/tags/', TagListCreateAPIView.as_view(), name='tag-list'),
    path('tasks/<int:task_pk>/tags/<int:pk>/', TagDetailAPIView.as_view(), name='tag-detail')
]
