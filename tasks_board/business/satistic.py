from datetime import date
from jinja2 import Template
from tasks_board.models import DailyTask, Goal


class Category:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks

    @property
    def done(self):
        return len(list(filter(lambda task: task.status, self.tasks)))

    @property
    def total_amount(self):
        return len(self.tasks)

    @property
    def percent(self):
        if not self.total_amount:
            return 100
        return int(round(self.done/self.total_amount, 2) * 100)

    @property
    def modal_id(self):
        return f'#{self.name.replace(" ", "")}'

    @property
    def modal_html(self):
        modal = Template(open('tasks_board/templates/tasks_board/statistic_plot_modal.html').read())
        return modal.render({'modal_id': self.modal_id[1:], 'name': self.name})


class Statistic:
    def __init__(self, request):
        self.request = request

    @property
    def today_tasks(self):
        tasks = DailyTask.objects.filter(owner=self.request.user, day=date.today())
        return Category('Today tasks', tasks)

    @property
    def all_tasks(self):
        tasks = DailyTask.objects.filter(owner=self.request.user)
        return Category('All tasks', tasks)

    @property
    def goals_tasks(self):
        result = []
        goals = Goal.objects.filter(owner=self.request.user)
        for goal in goals:
            goal_tasks = Category(goal.title, goal.tasks)
            result.append(goal_tasks)
        return result

