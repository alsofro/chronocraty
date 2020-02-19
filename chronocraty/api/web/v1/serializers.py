from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import Task, SubTask, Comment, User, Tag


class SubtaskSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    task = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='task-detail')

    class Meta:
        model = User
        exclude = ('confirmed', 'confirmed_date')

    def validate_password(self, value: str) -> str:
        return make_password(value)
