# TaskManagement/TaskProcessor.py
from aidonis_core.TaskManagement.TaskEndNotifier import TaskEndNotifier
from aidonis_core.TaskManagement.Task import Task
from multiprocessing import Pool
import time


class TaskProcessor:
    def __init__(self, api_key: str, assistants_base: dict,  max_tasks: int = 5, notifier: TaskEndNotifier = None):
        """TaskProcessor class is responsible for managing generation tasks and running them in parallel.
        :param api_key: OpenAI API key
        :param assistants_base: dict containing the id of each assistant (related to the API key) as it follows:
            {"PROCESS_GENERATOR": "<id1>", "GRAPHIC_GENERATOR": "<id2>", "REVIEWER": "<id3>"}

        :param max_tasks: Maximum number of tasks to run in parallel
        :param notifier: TaskEndNotifier object, which can be inherited to create a custom response handler
        """

        self.api_key = api_key
        self.assistants_base = assistants_base
        self.max_tasks = max_tasks
        self.pool = Pool(max_tasks)
        self.notifier = notifier
        self.tasks = []

    def add_task(self, task: Task) -> None:
        """
        Add a task to the processor
        :param task: Task object
        """
        while len(self.tasks) >= self.max_tasks:
            time.sleep(1)  # add a pause between checks
        self.tasks.append(task)
        self.pool.apply_async(task.run, args=(self.api_key, self.assistants_base), callback=self.remove_task)

    def remove_task(self, result: str) -> None:
        """
        Remove a task from the processor. It also notifies the notifier if it is not None
        :param result: Result of the task
        """
        if self.notifier is not None:
            self.notifier.task_ended(self.tasks[0], result)

        self.tasks.pop(0)

    def get_tasks(self) -> list:
        """
        Get the list of tasks
        :return: List of tasks
        """
        return self.tasks

    def close_and_join_pool(self) -> None:
        """
        Close and join the pool. This method should be called when the processor is no longer needed.
        :return: None
        """
        self.pool.close()
        self.pool.join()
