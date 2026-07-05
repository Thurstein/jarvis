from pathlib import Path

# ==========================
# Configuración general
# ==========================

ASSISTANT_NAME = "Jarvis"

MODEL = "qwen3:14b"

TEMPERATURE = 0.3

SYSTEM_PROMPT = (
    Path("prompts/system_prompt.txt")
    .read_text(encoding="utf-8")
)