from datetime import date

import matplotlib.pyplot as plt
from jinja2 import Template
from tasks_board.models import DailyTask, Goal


class Category:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks

    @property
    def done_amount(self):
        return len(list(filter(lambda task: task.status, self.tasks)))

    @property
    def undone_amount(self):
        return len(list(filter(lambda task: not task.status, self.tasks)))

    @property
    def total_amount(self):
        return len(self.tasks)

    @property
    def percent(self):
        if not self.total_amount:
            return 100
        return int(round(self.done_amount / self.total_amount, 2) * 100)

    @property
    def modal_id(self):
        return f'#{self.name.replace(" ", "")}'

    @property
    def low_tasks(self):
        return len(list(filter(lambda task: task.priority == 0, self.tasks)))

    @property
    def normal_tasks(self):
        return len(list(filter(lambda task: task.priority == 1, self.tasks)))

    @property
    def high_tasks(self):
        return len(list(filter(lambda task: task.priority == 2, self.tasks)))

    def productivity_chart(self):
        fig = plt.figure()
        fig.patch.set_facecolor('#A9A9A9')

        sections = ['Done', 'In progress']
        colors = ['g', '#343a40']

        slices = [self.done_amount, self.undone_amount]

        plt.pie(slices, labels=sections, colors=colors)
        img_path = f'static/tasks_board/images/charts/{self.modal_id[1:]}_chart1.svg'
        plt.savefig('tasks_board/' + img_path)
        plt.close()
        return img_path

    def priority_chart(self):
        labels = ['Low', 'Normal', 'High']

        men_means = self.low_tasks
        normal = self.normal_tasks
        high = self.high_tasks

        x = [0, 1, 2]
        width = 0.35

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#A9A9A9')
        rects1 = ax.bar(0, men_means, width, label='Low', color='#808080')
        rects2 = ax.bar(1, normal, width, label='Normal', color='#FFFF00')
        rects3 = ax.bar(2, high, width, label='High', color='#FF0000')

        ax.set_ylabel('Tasks number')
        ax.set_title('Tasks by priority')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        ax.bar_label(rects1, padding=2)
        ax.bar_label(rects2, padding=2)
        ax.bar_label(rects3, padding=2)

        fig.tight_layout()

        img_path = f'static/tasks_board/images/charts/{self.modal_id[1:]}_chart2.svg'
        plt.savefig('tasks_board/' + img_path)
        plt.close()
        return img_path

    @property
    def modal_html(self):
        modal = Template(open('tasks_board/templates/tasks_board/statistic_plot_modal.html').read())
        if self.total_amount:
            modal = modal.render({'modal_id': self.modal_id[1:],
                                  'name': self.name,
                                  'productivity': f'./{self.productivity_chart()}',
                                  'priority_ratio': f'./{self.priority_chart()}'
                                  })
        else:
            modal = modal.render({'modal_id': self.modal_id[1:],
                                  'name': self.name,
                                  'no_tasks': True
                                  })
        return modal


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