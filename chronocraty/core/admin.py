from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Tag, Task, SubTask, Comment

User = get_user_model()

admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Comment)
admin.site.register(User)
