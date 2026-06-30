from ollama import chat
import config


class Brain:

    def __init__(self):
        self.model = config.MODEL

    def ask(self, messages, tools=None):

        response = chat(
            model=self.model,
            messages=messages,
            tools=tools
        )

        return response.message

    def continue_chat(self, messages):

        response = chat(
            model=self.model,
            messages=messages
        )

        return response.message