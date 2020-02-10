from rest_framework import serializers

from core.models import Task, SubTask, Comment, User, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'tasks', 'confirmed', 'confirmed_date', 'email')


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('date_created', 'date_updated')


class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    users = UserSerializer(many=True)

    class Meta:
        model = Task
        exclude = ('is_active',)

