class Conversation:

    def __init__(self, system_prompt):

        self.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    def add_user(self, message):

        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant(self, message):

        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def add_tool_call(self, response):

        self.messages.append({
            "role": "assistant",
            "content": response.content or "",
            "tool_calls": response.tool_calls
        })

    def add_tool_result(self, tool_name, result):

        self.messages.append({
            "role": "tool",
            "name": tool_name,
            "content": result
        })

    def get_messages(self):

        return self.messages

    def clear(self):

        system = self.messages[0]
        self.messages = [system]