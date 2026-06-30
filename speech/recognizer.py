import tempfile
import wave
import numpy as np
import sounddevice as sd
import torch
import whisper
import keyboard  
import time

class SpeechRecognizer:

    def __init__(self, model_name="small"):
        print("Cargando Whisper...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Usando dispositivo: {self.device}")
        
        self.model = whisper.load_model(model_name, device=self.device)
        print("Whisper listo.")

    def listen(self):
        samplerate = 16000
        audio_chunks = []
        
        # Definimos la tecla de Push-to-Talk:
        ptt_key = "f8"
        
        print(f"\n[Mantén presionada la F8 para hablar...]")
        
        # 1. Esperar a que el usuario presione la tecla por primera vez
        keyboard.wait(ptt_key)
        print("-> Grabando... (Suelta la tecla para detener)")

        # Callback que se ejecuta cada vez que el micrófono recibe audio
        def callback(indata, frames, time, status):
            if status:
                print(status)
            # Solo guardamos el audio si la tecla sigue presionada
            if keyboard.is_pressed(ptt_key):
                audio_chunks.append(indata.copy())

        # 2. Abrir el stream de audio en segundo plano
        with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16', callback=callback):
            # Mantener el stream vivo mientras la tecla esté presionada
            while keyboard.is_pressed(ptt_key):
                time.sleep(0.05) # Pequeña pausa para no saturar el procesador

        print("-> Grabación finalizada. Procesando audio...")

        if not audio_chunks:
            print("No se grabó ningún audio.")
            return ""

        # Concatenamos todos los fragmentos capturados
        audio_data = np.concatenate(audio_chunks, axis=0)

        # 3. Guardar en archivo temporal y transcribir
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            with wave.open(tmp.name, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2) # 16 bits = 2 bytes
                wav.setframerate(samplerate)
                wav.writeframes(audio_data.tobytes())

            result = self.model.transcribe(tmp.name, language="es")

        text = result["text"]
        return text.strip() if isinstance(text, str) else ""