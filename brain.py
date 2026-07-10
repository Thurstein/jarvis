import ollama
import config
import time

class Brain:

    def __init__(self):
        self.model = config.MODEL
        self.temperature = config.TEMPERATURE

    def chat(self, messages, tools=None):

        start = time.perf_counter()

        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=tools,
            options={
                "temperature": self.temperature,
                "num_predict": 500
            }
        )

        print(
            f"[Ollama] "
            f"{time.perf_counter() - start:.2f}s"
        )

        print(
            f"[Tokens] "
            f"{response.eval_count}"
        )

        print(
            f"[Eval duration] "
            f"{response.eval_duration}"
        )

        return response.message