from tasks_board.models import DailyTask, Goal
from datetime import date


def save_task_form(request):
    task = DailyTask()
    task.title = request.POST.get('title')
    day = request.POST.get('date')
    if day:
        try:
            task.date = date.fromisoformat(day)
        except ValueError:
            return 'date error'
    goal = request.POST.get('goal')
    if goal:
        task.goal = Goal.objects.get(pk=goal)
    priority = request.POST.get('priority')
    if priority:
        task.priority = priority
    status = request.POST.get('status')
    task.status = True if status == 'true' else False
    task.owner = request.user
    task.save()
    return 'ok'
