import json
import pytz
from datetime import datetime

from django.urls import reverse
from django.test import TestCase
from django.test.client import Client
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate


from api.web.v1.views import TaskListCreateAPIView, TaskDetailAPIView, UserListCreateAPIView, \
    UserDetailAPIView, SubtaskListCreateAPIView, SubtaskDetailAPIView, CommentListCreateAPIView, \
    CommentDetailAPIView, TagListCreateAPIView, TagDetailAPIView
from core.models import Task, SubTask, User, Comment, Tag


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

    def test_api_detal_task(self):
        user = User.objects.get(email='mail@mail.ru')
        user_id = user.id
        
        factory = APIRequestFactory()
        data = {
            "title": "Task1",
            "description": "Task1 description",
            "date_expired": datetime(2025,1,1,12,0,0, tzinfo=pytz.UTC),
            "is_active": True,
            "color": "#331122",
            "priority": 1,
            "user": user
        }
        task = Task.objects.create(**data)
        task.save()
        view = TaskDetailAPIView.as_view()
        request = factory.get('/api/tasks/{0}/'.format(task.id))
        force_authenticate(request, user=user)
        response = view(request, pk=task.id)
        received_data = json.loads(response.rendered_content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'],       received_data['title'])
        self.assertEqual(data['description'], received_data['description'])
        self.assertEqual(data['is_active'],   received_data['is_active'])
        self.assertEqual(data['color'],       received_data['color'])
        self.assertEqual(data['priority'],    received_data['priority'])
        self.assertEqual('mail@mail.ru',      received_data['user'])


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
        received_data = json.loads(response.rendered_content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(first_name='John').username, 'John Smith')

class TestSubTasksAPI(TestCase):
    def setUp(self):
        user = User.objects.create_user('mail@mail.ru', password='password', is_active=True, is_staff=True, is_admin=True)
        Task.objects.create(**{
            "title": "Task1",
            "description": "Task1 description",
            "date_expired": datetime(2025,1,1,12,0,0, tzinfo=pytz.UTC),
            "is_active": True,
            "color": "#331122",
            "priority": 1,
            "user": user
        })
        self.assertEqual.__self__.maxDiff = None

    def test_api_create_subtask(self):
        task = Task.objects.get(title='Task1')
        user = User.objects.get(email='mail@mail.ru')
        user_id = user.id
        factory = APIRequestFactory()
        data = {
            "title": "SubTask1",
            "description": "SubTask1 description",
            "date_expired": "2025-01-01T12:00:00+03:00",
            "is_active": True,
            "position": 100,
            "color": "#331122",
            "user_pk": user_id,
            "task": task.id
        }
        view = SubtaskListCreateAPIView.as_view()
        request = factory.post('/api/tasks/{0}/subtasks'.format(task.id), json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = view(request, task_pk=task.id)
        received_data = json.loads(response.rendered_content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['title'],       received_data['title'])
        self.assertEqual(data['description'], received_data['description'])
        self.assertEqual(data['date_expired'],received_data['date_expired'])
        self.assertEqual(data['is_active'],   received_data['is_active'])
        self.assertEqual(data['position'],    received_data['position'])
        self.assertEqual(data['color'],       received_data['color'])
        self.assertEqual(task.title,          received_data['task'])

    def test_api_detal_subtask(self):
        user = User.objects.get(email='mail@mail.ru')
        user_id = user.id
        factory = APIRequestFactory()
        task = Task.objects.get(title='Task1')

        subtask_data = {
            "title": "SubTask1",
            "description": "SubTask1 description",
            "date_expired": datetime(2025,1,1,12,0,0, tzinfo=pytz.UTC),
            "is_active": True,
            "color": "#331122",
            "position": 100,
            "task": task
        }
        subtask = SubTask.objects.create(**subtask_data)
        task.save()

        view = SubtaskDetailAPIView.as_view()
        request = factory.get('/api/tasks/{0}/subtasks/{1}/'.format(task.id, subtask.id))
        force_authenticate(request, user=user)
        response = view(request, task_pk=task.id, pk=subtask.id)
        received_data = json.loads(response.rendered_content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(subtask_data['title'],       received_data['title'])
        self.assertEqual(subtask_data['description'], received_data['description'])
        self.assertEqual(subtask_data['is_active'],   received_data['is_active'])
        self.assertEqual(subtask_data['color'],       received_data['color'])
        self.assertEqual(subtask_data['position'],    received_data['position'])
        self.assertEqual(task.title,      received_data['task'])

class TestCommentsAPI(TestCase):
    def setUp(self):
        user = User.objects.create_user('mail@mail.ru', password='password', is_active=True, is_staff=True, is_admin=True)
        Task.objects.create(**{
            "title": "Task1",
            "description": "Task1 description",
            "date_expired": datetime(2025,1,1,12,0,0, tzinfo=pytz.UTC),
            "is_active": True,
            "color": "#331122",
            "priority": 1,
            "user": user
        })
        self.assertEqual.__self__.maxDiff = None

    def test_api_create_comment(self):
        task = Task.objects.get(title='Task1')
        user = User.objects.get(email='mail@mail.ru')
        user_id = user.id
        factory = APIRequestFactory()
        data = {
            "body": "Comment1 of Task1",
            "user_pk": user_id,
            "task": task.id
        }
        view = CommentListCreateAPIView.as_view()
        request = factory.post('/api/tasks/{0}/comments'.format(task.id), json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = view(request, task_pk=task.id)
        received_data = json.loads(response.rendered_content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['body'], received_data['body'])
        self.assertEqual(user.email,   received_data['user'])
        self.assertEqual(task.title,   received_data['task'])

    def test_api_detal_comment(self):
        user = User.objects.get(email='mail@mail.ru')
        task = Task.objects.get(title='Task1')
        user_id = user.id
        factory = APIRequestFactory()
        data = {
            "body": "Comment1 of Task1",
            "task": task,
            "user": user
        }
        comment = Comment.objects.create(**data)
        comment.save()
        view = CommentDetailAPIView.as_view()
        request = factory.get('/api/tasks/{0}/comments/{1}/'.format(task.id, comment.id))
        force_authenticate(request, user=user)
        response = view(request, task_pk=task.id, pk=comment.id)
        received_data = json.loads(response.rendered_content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['body'], received_data['body'])
        self.assertEqual(task.title,   received_data['task'])
        self.assertEqual(user.email,   received_data['user'])

class TestTagsAPI(TestCase):
    def setUp(self):
        user = User.objects.create_user('mail@mail.ru', password='password', is_active=True, is_staff=True, is_admin=True)
        Task.objects.create(**{
            "title": "Task1",
            "description": "Task1 description",
            "date_expired": datetime(2025,1,1,12,0,0, tzinfo=pytz.UTC),
            "is_active": True,
            "color": "#331122",
            "priority": 1,
            "user": user
        })
        self.assertEqual.__self__.maxDiff = None

    def test_api_create_tag(self):
        task = Task.objects.get(title='Task1')
        task_id = task.id
        user = User.objects.get(email='mail@mail.ru')
        factory = APIRequestFactory()
        data = {
            "name": "Tag1 of Task1",
            "task": task_id
        }
        view = TagListCreateAPIView.as_view()
        request = factory.post('/api/tasks/{0}/tags'.format(task.id), json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = view(request, task_pk=task.id)
        received_data = json.loads(response.rendered_content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['name'], received_data['name'])
        self.assertEqual(task.title,   received_data['task'])

    def test_api_detal_tag(self):
        user = User.objects.get(email='mail@mail.ru')
        task = Task.objects.get(title='Task1')
        # user_id = user.id
        factory = APIRequestFactory()
        data = {
            "name": "Tag1 of Task1",
            "task": task
        }
        tag = Tag.objects.create(**data)
        tag.save()
        view = TagDetailAPIView.as_view()
        request = factory.get('/api/tasks/{0}/tags/{1}/'.format(task.id, tag.id))
        force_authenticate(request, user=user)
        response = view(request, task_pk=task.id, pk=tag.id)
        received_data = json.loads(response.rendered_content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], received_data['name'])
        self.assertEqual(task.title,   received_data['task'])
        