import threading


class Task(threading.Thread):

    def __int__(self, prompt, file_url=None):
        self.prompt = prompt
        self.file_url = file_url

