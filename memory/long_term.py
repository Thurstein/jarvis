from pathlib import Path
import json

MEMORY_FILE = Path("memory/memory.json")

memory = {}

def _load():
    """
    Carga la memoria desde el archivo JSON.
    """

    global memory

    if not MEMORY_FILE.exists():
        return

    try:

        with MEMORY_FILE.open(
            "r",
            encoding="utf-8"
        ) as f:

            memory = json.load(f)

    except json.JSONDecodeError:

        memory = {}

def _save():
    """
    Guarda la memoria en el archivo JSON.
    """

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with MEMORY_FILE.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory,
            f,
            ensure_ascii=False,
            indent=4
        )

def remember(key: str, value):
    """
    Guarda un recuerdo permanente.
    """

    _load()

    memory[key] = value

    _save()


def recall(key: str, default=None):
    """
    Recupera un recuerdo permanente.
    """
    return memory.get(key, default)


def forget(key: str):
    """
    Elimina un recuerdo.
    """
    memory.pop(key, None)

def remember_text(key: str, value: str) -> str:
    """
    Guarda un dato en la memoria permanente.
    """

    remember(key, value)

    return f"Recordaré '{key}'."


def recall_text(key: str) -> str:
    """
    Recupera un dato de la memoria permanente.
    """

    value = recall(key)

    if value is None:
        return "No tengo ningún recuerdo con ese nombre."

    return str(value)

_load()