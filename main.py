import config

from core.assistant import Assistant
from prompts import SYSTEM_PROMPT
from tools.filesystem import find_file, open_file, open_in_explorer

from tools.programs import open_program
from tools.browser import open_url
from tools.volume import set_volume
from tools.media import (
    play_pause,
    next_track,
    previous_track,
    stop_media,
)

from memory.long_term import (
    remember_text,
    recall_text,
)

from speech.recognizer import SpeechRecognizer
from speech.tts import TextToSpeech


assistant = Assistant(
    SYSTEM_PROMPT,
    config.ASSISTANT_NAME
)

#Registros de herramientas:
assistant.register_tools([
    open_program,
    open_url,
    set_volume,

    play_pause,
    next_track,

    previous_track,
    stop_media,
    find_file,
    open_in_explorer,
    open_file,

    remember_text,
    recall_text
])

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