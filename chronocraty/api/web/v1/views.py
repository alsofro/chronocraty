from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import permissions

from core.models import (
    Task,
    SubTask,
    Comment,
    Tag
)
from .serializers import (
    UserSerializer,
    TaskSerializer,
    SubtaskSerializer,
    CommentSerializer,
    TagSerializer
)

User = get_user_model()


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SubtaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        task_pk = self.kwargs.get('task_pk')
        task = get_object_or_404(Task, pk=task_pk)
        serializer.save(task=task)


class SubtaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        task_pk = self.kwargs.get('task_pk')
        task = get_object_or_404(Task, pk=task_pk)
        user = self.request.user
        serializer.save(task=task, user=user)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        task_pk = self.kwargs.get('task_pk')
        if task_pk:
            task = get_object_or_404(Task, pk=task_pk)
            serializer.save(task=task)
        serializer.save()


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
