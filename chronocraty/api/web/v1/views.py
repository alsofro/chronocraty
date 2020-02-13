from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.generics import get_object_or_404

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

    def perform_create(self, serializer):
        user_pk = self.request.data.get('user_pk')
        user = get_object_or_404(User, pk=user_pk)
        serializer.save(user=user)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SubtaskCreateAPIView(generics.CreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskSerializer

    def perform_create(self, serializer):
        task_pk = self.request.data.get('task_pk')
        task = get_object_or_404(Task, pk=task_pk)
        serializer.save(task=task)


class SubtaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        task_pk = self.request.data.get('task_pk')
        task = get_object_or_404(Task, pk=task_pk)
        serializer.save(task=task)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TagListAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        task_pk = self.request.data.get('task_pk')
        if task_pk:
            task = get_object_or_404(Task, pk=task_pk)
            serializer.save(task=task)
        serializer.save()


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
