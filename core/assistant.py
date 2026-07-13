from brain import Brain
from memory.long_term import search_memory
from core.conversation import Conversation
from core.tool_manager import ToolManager
import time

class Assistant:

    def __init__(self, system_prompt, name="Jarvis"):

        self.name = name

        self.brain = Brain()

        self.conversation = Conversation(system_prompt)

        self.tool_manager = ToolManager()

    def register_tool(self, tool):

        self.tool_manager.register(tool)

    def register_tools(self, tools):

        for tool in tools:
            self.tool_manager.register(tool)

    def process(self, user_message):

        start_time = time.perf_counter()

        self.conversation.messages = [
            m
            for m in self.conversation.messages
            if not (
                m["role"] == "system"
                and m.get("content", "").startswith(
                    "INFORMACIÓN DE MEMORIA."
                )
            )
        ]

        self.conversation.add_user(user_message)

        memory_result = search_memory(user_message)

        print("\n[Memory result]")
        print(memory_result)
        print()

        if memory_result != "No encontré recuerdos relacionados.":

            self.conversation.add_system(
                (
                    "INFORMACIÓN DE MEMORIA.\n"
                    "La siguiente información responde "
                    "directamente a la consulta actual.\n"
                    "Debes responder usando esta información.\n"
                    "NO uses herramientas.\n"
                    "NO busques archivos.\n"
                    "NO solicites información adicional.\n"
                    "NO hagas suposiciones.\n\n"
                    f"{memory_result}"
                )
            )

        llm_start = time.perf_counter()

        print(
            f"[Mensajes] "
            f"{len(self.conversation.get_messages())}"
        )

        print(
            f"[Caracteres contexto] "
            f"{sum(len(str(m.get('content', '')))
                    for m in self.conversation.get_messages())}"
        )

        response = self.brain.chat(
            self.conversation.get_messages(),
            self.tool_manager.get_tools()
        )

        print(
            f"[LLM inicial] "
            f"{time.perf_counter() - llm_start:.2f}s"
        )

        while response.tool_calls:

            # Guardamos la respuesta original del modelo
            self.conversation.add_tool_call(response)

            # Ejecutamos todas las herramientas solicitadas
            for tool in response.tool_calls:

                result = self.tool_manager.execute(tool)

                self.conversation.add_tool_result(
                    tool.function.name,
                    result
                )

            # El modelo continúa la conversación
            llm_tool_start = time.perf_counter()

            response = self.brain.chat(
                self.conversation.get_messages(),
                self.tool_manager.get_tools()
            )

            print(
                f"[LLM post-tool] "
                f"{time.perf_counter() - llm_tool_start:.2f}s"
            )

        elapsed = time.perf_counter() - start_time

        print(
            f"\n[Tiempo total] {elapsed:.2f}s"
        )

        self.conversation.add_assistant(
            response.content
        )

        return response.content
