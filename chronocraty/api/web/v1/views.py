from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from core.models import Task
from .serializers import TaskSerializer

User = get_user_model()


class TaskView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SingleTaskView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
