import multiprocessing
import ThreadedTask, TaskEndNotifier
from app import utils

class TaskProcessor(multiprocessing.Pool):
    def __init__(self, max_tasks=5, notifier:TaskEndNotifier=None):
        super().__init__(max_tasks)
        self.notifier = notifier
        self.tasks = []

    def add_task(self, task:ThreadedTask):
        self.tasks.append(task)
        self.apply_async(task.run, callback=self.remove_task)

    def remove_task(self, result):
        #Notify task listener
        if self.notifier is not None:
            self.notifier.task_ended(result)

        self.tasks.pop(0)

    def get_tasks(self):
        return self.tasks