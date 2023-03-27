from django.db import models
from django.contrib.auth.models import User

class tasks(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null = False, blank = False)
    description = models.TextField(null = True, blank = True)
    is_completed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
        db_table = 'tasks'

class steps(models.Model):
    task_id = models.ForeignKey('tasks', on_delete=models.CASCADE, related_name='steps')
    description = models.CharField(max_length=140, null = False, blank = False)
    is_completed = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'step'
        verbose_name_plural = 'steps'
        db_table = 'steps'