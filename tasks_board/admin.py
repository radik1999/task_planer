from django.contrib import admin

from .models import Goal, DailyTask

admin.site.register(Goal)
admin.site.register(DailyTask)
