# TaskManagement/TaskProcessor.py
import multiprocessing
from TaskManagement.TaskEndNotifier import TaskEndNotifier
from TaskManagement.Task import Task
from multiprocessing import Pool
import time

class TaskProcessor:
    def __init__(self, max_tasks=5, notifier: TaskEndNotifier = None):
        self.max_tasks = max_tasks
        self.pool = Pool(max_tasks)
        self.notifier = notifier
        self.tasks = []

    def add_task(self, task: Task):
        while len(self.tasks) >= self.max_tasks:
            time.sleep(1)  # Wait for a task to complete
        self.tasks.append(task)
        self.pool.apply_async(task.run, callback=self.remove_task)

    def remove_task(self, result):
        if self.notifier is not None:
            print(f"Task {result} is completed")
            self.notifier.task_ended(result)
        self.tasks.pop(0)
        print(f"Task {result} is removed")

    def get_tasks(self):
        return self.tasks

    def close_and_join_pool(self):
        self.pool.close()
        self.pool.join()