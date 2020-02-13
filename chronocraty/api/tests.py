import json
from datetime import datetime

from django.urls import reverse
from django.test import TestCase
from django.test.client import Client
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient


from api.web.v1.views import TaskListCreateAPIView
from core.models import Task, User


# Create your tests here.


class TestTasksAPI(TestCase):
    def setUp(self):
        User.objects.create_user('mail@mail.ru', password='password', is_active=True, is_staff=True, is_admin=True)
        self.assertEqual.__self__.maxDiff = None

    def test_api_create_task(self):
        user_id = User.objects.get(email='mail@mail.ru').id
        factory = APIRequestFactory()
        data = {
            "title": "Task1",
            "description": "Task1 description",
            "date_expired": "2025-01-01T12:00",
            "is_active": True,
            "color": "#331122",
            "priority": 1,
            "user_pk": user_id
        }
        view = TaskListCreateAPIView.as_view()
        request = factory.post('/api/tasks/', json.dumps(data), content_type='application/json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Task1')
