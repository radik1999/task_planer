from tasks_board.models import DailyTask, Goal
from datetime import date


def save_task_form(request, task_to_edit=None):
    task = task_to_edit if task_to_edit else DailyTask()

    title = request.POST.get('title')
    if not title:
        return 'blank title'
    else:
        task.title = title

    day = request.POST.get('date')
    if day:
        try:
            task.day = date.fromisoformat(day)
        except ValueError:
            return 'date error'

    goal = request.POST.get('goal')
    if goal:
        task.goal = Goal.objects.get(pk=goal)

    priority = request.POST.get('priority')
    if priority:
        task.priority = priority

    main_task = request.POST.get('main_task')
    if main_task:
        task.main_task = DailyTask.objects.get(pk=main_task)

    status = request.POST.get('status')
    task.status = True if status == 'true' else False

    task.owner = request.user

    task.save()
    return 'ok'


def save_goal_form(request, goal_to_edit=None):
    goal = goal_to_edit if goal_to_edit else Goal()

    title = request.POST.get('title')
    if not title:
        return 'blank title'
    else:
        goal.title = title

    priority = request.POST.get('priority')
    if priority:
        goal.priority = priority

    goal.owner = request.user

    goal.save()
    return 'ok'


def change_task_status(task: DailyTask):
    if not task.status:
        task.status = True
        for sub_task in task.sub_tasks:
            sub_task.status = True
            sub_task.save()
    else:
        task.status = False
    task.save()
