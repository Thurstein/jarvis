from brain import Brain

from core.conversation import Conversation
from core.tool_manager import ToolManager


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

        self.conversation.add_user(user_message)

        response = self.brain.ask(
            self.conversation.get_messages(),
            self.tool_manager.get_tools()
        )

        # Si el modelo solicita herramientas
        if response.tool_calls:

            # Guardamos la respuesta original del modelo
            self.conversation.add_tool_call(response)

            # Ejecutamos todas las herramientas solicitadas
            for tool in response.tool_calls:

                result = self.tool_manager.execute(tool)

                self.conversation.add_tool_result(
                    tool.function.name,
                    result
                )

            # El modelo continúa la conversación con el nuevo contexto
            final_response = self.brain.continue_chat(
                self.conversation.get_messages()
            )

            self.conversation.add_assistant(
                final_response.content
            )

            return final_response.content

        # Respuesta normal
        self.conversation.add_assistant(
            response.content
        )

        return response.content
    