import time

from openai import OpenAI


class AssistantConnector:

    def __init__(self, api_key, assistant_id):
        """
        AssistantConnector class is responsible for connecting to the OpenAI API and sending requests to the assistant.

        :param api_key: OpenAI API key
        :param assistant_id: Assistant ID where the requests will be sent
        """

        self.api_key = api_key
        self.assistant_id = assistant_id
        self.client = OpenAI(api_key=self.api_key)
        self.thread = None

    def get_thread_id(self):
        """
        Get the current thread ID
        :return: Thread ID
        """
        return self.thread.id

    def continue_thread(self, thread: str):
        """
        Continue a thread that was previously created.
        :param thread: Thread ID to be continued
        """
        self.thread = self.client.beta.threads.retrieve(thread)
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant_id
        )

        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)  # add a pause between checks
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

        # Get the assistant's response
        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )

            for message in messages.data:
                if message.role == 'assistant':
                    for content in message.content:
                        # Return the assistant's response
                        return content.text.value

        else:
            # Return an error message
            return "Error: " + run.status

    def generate_completion(self, prompt, file=None, **kwargs: dict):
        """
        Send a request to the assistant to generate a completion based on the given prompt.
        :param prompt:  The prompt to be sent to the assistant
        :param kwargs: Additional tweaking information to be sent to the assistant
        :return:  Assistant's response
        """

        # Create a new thread for the assistant
        global ass_file
        self.thread = self.client.beta.threads.create()

        if file:
            ass_file = self.client.files.create(
                file=open(file, "rb"),
                purpose='assistants'
            )

            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content="(File retrieval needed)",
                file_ids=[ass_file.id]
            )

        else:
            # Send the prompt to the assistant
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=prompt
            )

        if kwargs:
            string = ""
            for key, value in kwargs.items():
                # Send additional tweaking information to the assistant
                string += f"{key}={value}\n"

            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=string
            )
        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant_id
        )

        # Wait for the assistant to complete the task
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)  # add a pause between checks
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

        # Get the assistant's response
        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )

            file_deletion = self.client.files.delete(
                file_id=ass_file.id
            )

            for message in messages.data:
                if message.role == 'assistant':
                    for content in message.content:
                        # Return the assistant's response
                        return content.text.value

        else:
            # Return an error message
            return "Error: " + run.status
