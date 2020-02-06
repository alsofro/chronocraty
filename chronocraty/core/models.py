from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import PermissionsMixin

# validators

def validate_username(username):
    if len(username) < 3:
        raise ValidationError('Username must contain at least 3 characters')


# abstract models

class BaseAbstractCommonModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(BaseAbstractCommonModel):
    title = models.CharField(max_length=64, db_index=True)
    description = models.TextField(blank=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class TaskBaseModel(BaseModel):
    date_expired = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=True)
    color = models.CharField(max_length=16, default='#1456ab#103265')

    class Meta:
        abstract = True


# models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user_obj

    def create_superuser(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user_obj


class User(BaseAbstractCommonModel, AbstractBaseUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=32, blank=True, null=True, unique=True, validators=[validate_username])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    confirmed = models.BooleanField(default=False)
    confirmed_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=256, blank=True, null=True)
    tasks = models.ManyToManyField('Task', blank=True, related_name='users')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if not self.first_name and self.last_name:
            return self.email
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        if not self.first_name:
            return self.email
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class Task(TaskBaseModel):
    priority = models.PositiveSmallIntegerField()
    tags = models.ManyToManyField('Tag', blank=True, related_name='tasks')
    subtasks = models.ManyToManyField('SubTask', blank=True, related_name='tasks')
    comments = models.ManyToManyField('Comment', blank=True, related_name='tasks')


class SubTask(TaskBaseModel):
    position = models.FloatField()


class Comment(BaseModel):
    pass


class Tag(BaseModel):
    pass
