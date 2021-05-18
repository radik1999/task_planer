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
