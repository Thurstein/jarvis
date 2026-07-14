import asyncio
import os
import tempfile

import edge_tts
from playsound3 import playsound


class TextToSpeech:

    def __init__(self):

        self.voice = "es-CL-LorenzoNeural"
        # self.voice = "es-ES-AlvaroNeural"
        # self.voice = "es-MX-JorgeNeural"
        

    async def _generate(self, text, filename):

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate="+10%",
            pitch="-5Hz"
        )

        await communicate.save(filename)

    def _clean_text(self, text: str) -> str:

        # Ocultar rutas completas de Windows
        import re

        text = re.sub(
            r"[A-Za-z]:\\[^\s]+",
            "esa ubicación",
            text
        )

        return (
            text.replace("#", "")
                .replace("*", "")
                .replace("`", "")
                .replace("\\", "/")
                .replace("\n\n", "\n")
                .strip()
        )

    def speak(self, text):

        text = self._clean_text(text)

        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False
        ) as tmp:

            filename = tmp.name

        asyncio.run(
            self._generate(text, filename)
        )

        playsound(filename)

        os.remove(filename)