from django.db import models


# class User(models.Model):
#     pass

class BaseModel(models.Model):
    title = models.CharField(max_length=64, db_index=True)
    description = models.TextField(blank=True, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# class Status(BaseModel):
#     pass


class Tag(BaseModel):
    pass


class TaskBaseModel(BaseModel):
    date_expired = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=True)
    color = models.CharField(max_length=16, default='#1456ab#103265')

    # status = models.ForeignKey('Status', blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Task(TaskBaseModel):
    priority = models.PositiveSmallIntegerField()
    tags = models.ManyToManyField('Tag', blank=True, related_name='tasks')
    subtasks = models.ManyToManyField('SubTask', blank=True, related_name='tasks')
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)


class SubTask(TaskBaseModel):
    position = models.FloatField()
