from ollama import chat
import config


class Brain:

    def __init__(self):
        self.model = config.MODEL
        self.temperature = config.TEMPERATURE

    def ask(self, messages, tools=None):

        return self.chat(
            messages,
            tools
        )

    def continue_chat(self, messages):

        return self.chat(messages)
    
    def chat(self, messages, tools=None):

        response = chat(
            model=self.model,
            messages=messages,
            tools=tools,
            options={
                "temperature": self.temperature
            }
        )

        return response.message