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
            print("Status: " + run.status)
            time.sleep(1)  # add a pause between checks
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

        # Get the assistant's response
        if run.status == 'completed':
            print("Assistant completed the task")
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )

            for message in messages.data:
                if message.role == 'assistant':
                    for content in message.content:
                        # Return the assistant's response
                        return content.text.value

        else:
            print("Assistant did not complete the task")
            print("Error: " + run.status)
            # Return an error message
            return "Error: " + run.status


    def generate_completion(self, prompt, **kwargs: dict):
        """
        Send a request to the assistant to generate a completion based on the given prompt.
        :param prompt:  The prompt to be sent to the assistant
        :param kwargs: Additional tweaking information to be sent to the assistant
        :return:  Assistant's response
        """

        # Create a new thread for the assistant
        self.thread = self.client.beta.threads.create()

        # Send the prompt to the assistant
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )

        if kwargs:
            print("Additional tweaking information:")
            print(kwargs)
            string = ""
            for key, value in kwargs.items():
                # Send additional tweaking information to the assistant
                string += f"{key}={value}\n"

            print("Additional tweaking information string:")
            print(string)

            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=string
            )

            print("Additional tweaking information sent to the assistant")

        print("Prompt sent to the assistant")

        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant_id
        )

        print("Assistant is running")

        # Wait for the assistant to complete the task
        while run.status in ['queued', 'in_progress', 'cancelling']:
            print("Status: " + run.status)
            time.sleep(1)  # add a pause between checks
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

        # Get the assistant's response
        if run.status == 'completed':
            print("Assistant completed the task")
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )

            for message in messages.data:
                if message.role == 'assistant':
                    for content in message.content:
                        # Return the assistant's response
                        return content.text.value

        else:
            print("Assistant did not complete the task")
            print("Error: " + run.status)
            # Return an error message
            return "Error: " + run.status
