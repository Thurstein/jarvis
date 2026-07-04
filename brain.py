import ollama
import config


class Brain:

    def __init__(self):
        self.model = config.MODEL
        self.temperature = config.TEMPERATURE
    
    def chat(self, messages, tools=None):

        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=tools,
            options={
                "temperature": self.temperature
            }
        )

        return response.message