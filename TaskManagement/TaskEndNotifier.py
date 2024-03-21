from abc import ABC, abstractmethod


class TaskEndNotifier(ABC):
    """
    Abstract class for task end notifier. This class should be inherited to create a custom response handler
    """
    @abstractmethod
    def task_ended(self, task, result):
        """
        Method to be called when a task ends
        :param task: Task object
        :param result: Result of the task
        """
        pass
