from memory import workspace

class ToolManager:

    def __init__(self):

        self.tools = {}

    def register(self, function):

        self.tools[function.__name__] = {
            "function": function,
            "description": function.__doc__ or ""
        }

    def get_tools(self):

        return [
            tool["function"]
            for tool in self.tools.values()
        ]

    def execute(self, tool_call):

        name = tool_call.function.name

        arguments = tool_call.function.arguments

        print(f"\n[Tool] {name}")
        print(f"[Args] {arguments}")

        if name not in self.tools:
            return f"La herramienta '{name}' no existe."

        function = self.tools[name]["function"]

        result = function(**arguments)

        print(f"[Result] {result}")

        print("\n[Workspace]")
        print(workspace.dump())
        print()

        return result

    def list_tools(self):

        return list(self.tools.keys())