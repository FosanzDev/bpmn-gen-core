import threading
import time
import uuid

from GenAI import AssistantConnector, Sculptor
from multiprocessing import Manager

class Task:
    def __init__(self, prompt, file_url=None):
        self.id = uuid.uuid4()
        self.prompt = prompt
        self.file_url = file_url
        manager = Manager()
        self.status = manager.dict()
        self.status[self.id] = "CREATED"

    def run(self, api_key, assistants_base):
        self.status[self.id] = "RUNNING"
        process_generator = AssistantConnector(api_key, assistants_base["PROCESS_GENERATOR"])
        graphic_generator = AssistantConnector(api_key, assistants_base["GRAPHIC_GENERATOR"])
        reviewer = AssistantConnector(api_key, assistants_base["REVIEWER"])
        sculptor = Sculptor()

        self.status[self.id] = "GENERATING PROCESS"
        time.sleep(3)
        # process = process_generator.generate_completion(self.prompt)

        self.status[self.id] = "GENERATING GRAPHIC"
        time.sleep(3)
        # graphic = graphic_generator.generate_completion(process)

        self.status[self.id] = "REVIEWING"
        time.sleep(3)
        # graphic_reviewed = reviewer.generate_completion(graphic)

        self.status[self.id] = "SCULPTING"
        time.sleep(3)
        # bpmn_content = sculptor.sculpt(process, graphic_reviewed)

        self.status[self.id] = "COMPLETED"
        return "<bpmn_content>"  # Return the bpmn content

    def get_status(self):
        return self.status[self.id]

    def get_id(self):
        return self.id