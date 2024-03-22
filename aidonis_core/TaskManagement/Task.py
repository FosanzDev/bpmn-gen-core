import uuid
from multiprocessing import Manager

from aidonis_core.GenAI import AssistantConnector, Sculptor


class Task:
    def __init__(self, prompt):
        """
        Task element is responsible for managing the task's status and running the process of generating a BPMN file.
        The <run> method is responsible for running the process and updating the status of the task. It is automatically
        managed by TaskProcessorClass in order to run in parallel with other tasks. In case you want to run a task
        individually, you can call the <run> method directly.

        :param prompt: Prompt to be sent to the assistant
        """
        self.id = uuid.uuid4()
        self.prompt = prompt
        manager = Manager()
        self.status = manager.dict()
        self.status[self.id] = "CREATED"

    def run(self, api_key: str, assistants_base: dict) -> str:
        """
        Run the process of generating a BPMN file with OpenAI's GPT-3.5 engine. This method is automatically called by
        TaskProcessor class when running in parallel with other tasks. In case you want to run a task individually, you
        will need to provide the api_key and assistants_base as parameters.
        :param api_key: OpenAI API key
        :param assistants_base: dict containing the id of each assistant (related to the API key) as it follows:
        {"PROCESS_GENERATOR": "<id1>", "GRAPHIC_GENERATOR": "<id2>", "REVIEWER": "<id3>"}
        :return: BPMN file content as a string
        """
        self.status[self.id] = "RUNNING"
        process_generator = AssistantConnector(api_key, assistants_base["PROCESS_GENERATOR"])
        graphic_generator = AssistantConnector(api_key, assistants_base["GRAPHIC_GENERATOR"])
        reviewer = AssistantConnector(api_key, assistants_base["REVIEWER"])
        sculptor = Sculptor()

        self.status[self.id] = "GENERATING PROCESS"
        process = process_generator.generate_completion(self.prompt)

        self.status[self.id] = "GENERATING GRAPHIC"
        graphic = graphic_generator.generate_completion(process)

        self.status[self.id] = "REVIEWING"
        graphic_reviewed = reviewer.generate_completion(graphic)

        self.status[self.id] = "SCULPTING"
        bpmn_content = sculptor.sculpt(process, graphic_reviewed)

        self.status[self.id] = "COMPLETED"
        return bpmn_content

    def get_status(self) -> str:
        """
        Return the status of the task. Actual statuses are:
        - CREATED
        - RUNNING
        - GENERATING PROCESS
        - GENERATING GRAPHIC
        - REVIEWING
        - SCULPTING
        - COMPLETED
        :return: Status of the task
        """
        return self.status[self.id]

    def get_id(self) -> uuid.UUID:
        """
        Return the id of the task
        :return: Id of the task
        """
        return self.id
