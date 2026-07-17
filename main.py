import config

from core.assistant import Assistant
from core.tool_registry import register_tools

from prompts import SYSTEM_PROMPT

from speech.recognizer import SpeechRecognizer
from speech.tts import TextToSpeech

assistant = Assistant(
    SYSTEM_PROMPT,
    config.ASSISTANT_NAME
)

#Registros de herramientas:
register_tools(assistant)

print(f"{config.ASSISTANT_NAME} iniciado.\n")


recognizer = SpeechRecognizer()
tts = TextToSpeech()

while True:

    user = recognizer.listen()

    if not user:
        continue

    user = user.strip()

    if len(user) < 2:
        continue

    print(f"\nTú: {user}")

    response = assistant.process(user)

    print(f"\n{config.ASSISTANT_NAME}:")
    print(response)
    print()

    tts.speak(response)