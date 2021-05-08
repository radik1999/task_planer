import datetime

from django.conf import settings
from django.db import models
from datetime import date


class Priority(models.IntegerChoices):
    LOW = 0, 'Low'
    NORMAL = 1, 'Normal'
    HIGH = 2, 'High'


class Goal(models.Model):
    title = models.CharField(max_length=128)
    priority = models.IntegerField(default=Priority.LOW, choices=Priority.choices)
    main_goal = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


class DailyTask(models.Model):
    title = models.CharField(max_length=128)
    priority = models.IntegerField(default=Priority.LOW, choices=Priority.choices)
    status = models.BooleanField(default=False)
    day = models.DateField(default=date.today())
    main_task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.title}: {self.status}'

    @property
    def get_priority(self):
        for choice in Priority.choices:
            if self.priority in choice:
                return choice[1]

    @property
    def color(self):
        bootstrap_colors = {'Low': 'gray', 'Normal': 'yellow', 'High': 'red'}
        return bootstrap_colors[self.get_priority]

    @property
    def sub_tasks(self):
        return DailyTask.objects.filter(owner=self.owner, main_task=self)
