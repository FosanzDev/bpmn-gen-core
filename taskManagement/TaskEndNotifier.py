from abc import ABC, abstractmethod

class TaskEndNotifier(ABC):
    @abstractmethod
    def task_ended(self, task):
        pass