from rest_framework import serializers

from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'date_created',
            'date_updated',
            'priority',
            'date_expired',
            'is_active',
            'color',
            'users',
            'tags',
            'subtasks',
            'comments'
        )
