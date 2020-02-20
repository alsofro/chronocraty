import json
from datetime import datetime

from django.urls import reverse
from django.test import TestCase
from django.test.client import Client
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate


from api.web.v1.views import TaskListCreateAPIView, UserListCreateAPIView
from core.models import Task, User


# Create your tests here.


class TestTasksAPI(TestCase):
    def setUp(self):
        User.objects.create_user('mail@mail.ru', password='password', is_active=True, is_staff=True, is_admin=True)
        self.assertEqual.__self__.maxDiff = None

    def test_api_create_task(self):
        user = User.objects.get(email='mail@mail.ru')
        user_id = user.id
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
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Task1')


class TestUsersAPI(TestCase):
    def setUp(self):
        User.objects.create_user('mail@mail.ru', password='password', is_active=True, is_staff=True, is_admin=True)
        self.assertEqual.__self__.maxDiff = None

    def test_api_list_user(self):
        user_id = User.objects.get(email='mail@mail.ru').id
        factory = APIRequestFactory()
        view = UserListCreateAPIView.as_view()
        request = factory.get('/api/users/')
        response = view(request)
        received_data = json.loads(response.rendered_content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(received_data[0]['email'], 'mail@mail.ru')

    def test_api_create_user(self):
        factory = APIRequestFactory()
        data = {
            "password": "password",
            "last_login": None,
            "first_name": "John",
            "last_name": "Smith",
            "email": "JohnSmith@mail.ru",
            "username": "John Smith",
            "is_active": True,
            "is_staff": True,
            "is_admin": True,
            "status": None
        }
        view = UserListCreateAPIView.as_view()
        request = factory.post('/api/users/', json.dumps(data), content_type='application/json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(first_name='John').username, 'John Smith')