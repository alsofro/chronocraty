from django.urls import path

from .views import (
    CommentDetailAPIView,
    TagListAPIView,
    SubtaskCreateAPIView,
    TaskListCreateAPIView,
    TaskListAPIView,
    TaskDetailAPIView,
    TaskDetailAPIView,
    TagDetailAPIView
)

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list'),

    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),

    path('tasks/<int:task_pk>/subtasks/', SingleTaskView.as_view(), name='task-subtask'),
    path('tasks/<int:task_pk>/comments/', SingleTaskView.as_view(), name='task-detail'),
    path('tasks/<int:task_pk>/tags/', SingleTaskView.as_view(), name='task-detail'),

    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetailAPIView.as_view(), name='tag-detail'),

    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),

]
