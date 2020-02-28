from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from core.utils.validators import validate_username


# abstract models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseTaskModel(BaseModel):
    title = models.CharField(max_length=64, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)
    date_expired = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    color = models.CharField(max_length=8, default='#1456ab')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


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


class User(BaseModel, AbstractBaseUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=128, blank=True, null=True, unique=True, validators=[validate_username])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    confirmed = models.BooleanField(default=False)
    confirmed_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=256, blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        if not self.first_name and not self.last_name:
            return self.email
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        if not self.first_name and not self.last_name:
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


class Task(BaseTaskModel):
    priority = models.PositiveSmallIntegerField(default=1)
    tags = models.ManyToManyField('Tag', blank=True, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')


class SubTask(BaseTaskModel):
    position = models.FloatField(default=10000)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')


class Comment(BaseModel):
    body = models.TextField(db_index=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.body


class Tag(BaseModel):
    name = models.CharField(max_length=64, db_index=True, unique=True)

    def __str__(self):
        return self.name
