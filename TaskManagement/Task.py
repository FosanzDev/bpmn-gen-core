# TaskManagement/Task.py
import time

class Task:
    def __init__(self, prompt, file_url=None):
        self.prompt = prompt
        self.file_url = file_url

    def run(self):
        print(f"Task {self.prompt} is running...")
        time.sleep(5)  # Simulate work with a sleep statement
        print(f"Task {self.prompt} has completed.")
        return self  # Return self