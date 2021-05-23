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
    def clean_name(self):
        return self.name.replace(" ", "").lower()

    @property
    def modal_id(self):
        return f'#{self.clean_name}'

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
        fig, ax = plt.subplots(figsize=(6, 4))

        fig.patch.set_facecolor('#343a40')

        sections = ['Done', 'In progress']
        colors = ['g', '#a9a9a9']
        slices = [self.done_amount, self.undone_amount]

        labels = ['{:10}{:>3}{:>5}%'.format(sections[0], slices[0], int((slices[0]/self.total_amount)*100))]
        labels += ['{:12}{:>3}{:>5}%'.format(sections[1], slices[1], int((slices[1]/self.total_amount)*100))]
        print(labels[0])
        print(labels[1])

        wedges, texts = plt.pie(slices, colors=colors, shadow=True)
        box = ax.get_position()
        ax.set_position([box.x0*0.5, box.y0, box.width, box.height])

        leg = ax.legend(wedges, labels,
                  bbox_to_anchor=(1, 0, 0.5, 1), loc="center left")

        hp = leg._legend_box.get_children()[1]
        for vp in hp.get_children():
            for row in vp.get_children():
                row.set_width(125)  # need to adapt this manually
                row.mode = "expand"
                row.align = "left"

        img_path = f'static/tasks_board/images/charts/{self.clean_name}_chart1.svg'
        plt.savefig('tasks_board/' + img_path)
        plt.close()
        return img_path

    def priority_chart(self):
        labels = ['Low', 'Normal', 'High']

        low = self.low_tasks
        normal = self.normal_tasks
        high = self.high_tasks

        x = [0, 1, 2]
        width = 0.35

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_facecolor('#343a40')
        fig.patch.set_facecolor('#343a40')

        rects1 = ax.bar(0, low, width, color='#808080')
        rects2 = ax.bar(1, normal, width, color='#FFFF00')
        rects3 = ax.bar(2, high, width, color='#FF0000')

        ax.set_xticks(x)
        ax.set_yticks([])
        ax.set_xticklabels(labels)

        ax.bar_label(rects1, padding=2)
        ax.bar_label(rects2, padding=2)
        ax.bar_label(rects3, padding=2)

        fig.tight_layout()

        img_path = f'static/tasks_board/images/charts/{self.clean_name}_chart2.svg'
        plt.savefig('tasks_board/' + img_path)
        plt.close()
        return img_path

    @property
    def modal_html(self):
        modal = Template(open('tasks_board/templates/tasks_board/statistic_plot_modal.html').read())
        if self.total_amount:
            modal = modal.render({'modal_id': self.clean_name,
                                  'name': self.name,
                                  'productivity': f'./{self.productivity_chart()}',
                                  'priority_ratio': f'./{self.priority_chart()}'
                                  })
        else:
            modal = modal.render({'modal_id': self.clean_name,
                                  'name': self.name,
                                  'no_tasks': True
                                  })
        return modal


class GoalCategory(Category):
    def __init__(self, goal_string_id):
        goal = Goal.objects.get(string_id=goal_string_id)
        self.goal_id = goal_string_id
        name = goal.title
        tasks = goal.tasks
        super().__init__(name, tasks)

    @property
    def clean_name(self):
        return self.goal_id


class Statistic:
    def __init__(self, request):
        self.request = request
        self.categories = {}

    @property
    def today_tasks(self):
        tasks = DailyTask.objects.filter(owner=self.request.user, day=date.today())
        today_tasks_category = Category('Today tasks', tasks)
        self.categories[today_tasks_category.clean_name] = today_tasks_category
        return today_tasks_category

    @property
    def all_tasks(self):
        tasks = DailyTask.objects.filter(owner=self.request.user)
        all_tasks_category = Category('All tasks', tasks)
        self.categories[all_tasks_category.clean_name] = all_tasks_category
        return all_tasks_category

    def goal_tasks(self, goal_string_id):
        return GoalCategory(goal_string_id)

    @property
    def goals_tasks(self):
        result = []
        goals = Goal.objects.filter(owner=self.request.user)
        for goal in goals:
            goal_tasks = Category(goal.title, goal.tasks)
            self.categories[goal_tasks.clean_name] = goal_tasks
            result.append(goal_tasks)
        return result
