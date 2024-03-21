# TaskManagement/TaskProcessor.py
import multiprocessing
from TaskManagement.TaskEndNotifier import TaskEndNotifier
from TaskManagement.Task import Task
from multiprocessing import Pool
import time


class TaskProcessor:
    def __init__(self, api_key: str, assistants_base: dict,  max_tasks: int = 5, notifier: TaskEndNotifier = None):
        """TaskProcessor class is responsible for managing generation tasks and running them in parallel.
        :param api_key: OpenAI API key
        :param assistants_base: dict containing the id of each assistant (related to the API key) as it follows:
            {"PROCESS_GENERATOR": "<id1>", "GRAPHIC_GENERATOR": "<id2>", "REVIEWER": "<id3>"}

        :param max_tasks: Maximum number of tasks to run in parallel
        :param notifier: TaskEndNotifier object
        """

        self.api_key = api_key
        self.assistants_base = assistants_base
        self.max_tasks = max_tasks
        self.pool = Pool(max_tasks)
        self.notifier = notifier
        self.tasks = []

    def add_task(self, task: Task):
        while len(self.tasks) >= self.max_tasks:
            time.sleep(1)  # Wait for a task to complete
        self.tasks.append(task)
        self.pool.apply_async(task.run, args=(self.api_key, self.assistants_base), callback=self.remove_task)


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
