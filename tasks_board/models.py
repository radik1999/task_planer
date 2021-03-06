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
    string_id = models.CharField(max_length=128)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.string_id = self.title.replace(" ", "").lower()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def get_priority(self):
        for choice in Priority.choices:
            if self.priority in choice:
                return choice[1]

    @property
    def color(self):
        colors = {'Low': 'gray', 'Normal': 'yellow', 'High': 'red'}
        return colors[self.get_priority]

    @property
    def bootstrap_color(self):
        bootstrap_colors = {'Low': 'secondary', 'Normal': 'warning', 'High': 'danger'}
        return bootstrap_colors[self.get_priority]

    @property
    def tasks(self):
        tasks = DailyTask.objects.filter(owner=self.owner, goal=self, main_task=None)
        tasks = sorted(tasks, key=lambda t: (not t.status, t.day, t.priority), reverse=True)
        return tasks


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
        if self.status:
            return 'green'
        colors = {'Low': 'gray', 'Normal': 'yellow', 'High': 'red'}
        return colors[self.get_priority]

    @property
    def bootstrap_color(self):
        if self.status:
            return 'success'
        bootstrap_colors = {'Low': 'secondary', 'Normal': 'warning', 'High': 'danger'}
        return bootstrap_colors[self.get_priority]

    @property
    def sub_tasks(self):
        tasks = DailyTask.objects.filter(owner=self.owner, main_task=self)
        tasks = sorted(tasks, key=lambda t: (t.day, t.priority), reverse=True)
        return tasks
