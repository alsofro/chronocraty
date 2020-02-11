from rest_framework import serializers

from core.models import Task, SubTask, Comment, User, Tag


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        exclude = ('task',)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        exclude = ('task',)


class TagSerializer(serializers.ModelSerializer):
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
        exclude = ('password', 'confirmed', 'confirmed_date', 'email')
