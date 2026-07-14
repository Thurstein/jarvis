import ollama
import config
import time

class Brain:

    def __init__(self):
        self.model = config.MODEL
        self.temperature = config.TEMPERATURE

    def chat(self, messages, tools=None):

        # print(
        #     f"[Messages] {len(messages)}"
        # )

        # print(
        #     f"[Caracteres contexto] "
        #     f"{sum(len(str(m)) for m in messages)}"
        # )

        start = time.perf_counter()

        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=tools,
            think=False,
            options={
                "temperature": self.temperature
            }
        )
        
        # print(
        #     f"[Ollama] "
        #     f"{time.perf_counter() - start:.2f}s"
        # )

        # print(
        #     f"[Prompt tokens] "
        #     f"{response.prompt_eval_count}"
        # )

        # print(
        #     f"[Tokens] "
        #     f"{response.eval_count}"
        # )

        # print(
        #     f"[Eval duration] "
        #     f"{response.eval_duration}"
        # )

        return response.message