from django.contrib import admin

from .models import Tag, Task, SubTask

admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(SubTask)
