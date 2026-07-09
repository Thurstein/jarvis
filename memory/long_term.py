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

    _load()

    return memory.get(key, default)

def forget(key: str):
    """
    Elimina un recuerdo.
    """

    _load()

    memory.pop(key, None)

    _save()

def remember_text(key: str, value: str) -> str:
    """
    Guarda información importante sobre el usuario,
    sus preferencias, gustos, datos personales,
    hardware, proyectos o cualquier dato que deba
    recordarse entre conversaciones.
    """

    remember(key, value)

    return f"Recordaré '{key}'."

def recall_text(key: str) -> str:
    """
    Recupera información previamente recordada
    sobre el usuario, sus preferencias, gustos,
    datos personales, hardware, proyectos u otros
    recuerdos almacenados.
    """

    value = recall(key)

    if value is None:
        return "No tengo ningún recuerdo con ese nombre."

    return str(value)

def keys():
    """
    Devuelve todas las claves almacenadas
    en la memoria permanente.
    """

    return list(memory.keys())

def items():
    """
    Devuelve una copia completa
    de la memoria permanente.
    """

    return dict(memory)

def list_memories() -> str:
    """
    Muestra todos los recuerdos disponibles
    almacenados en la memoria permanente.
    """

    memory_keys = keys()

    if not memory_keys:
        return "No hay recuerdos almacenados."

    return ", ".join(memory_keys)

def search_memory(query: str) -> str:
    """
    Busca recuerdos relacionados con una palabra
    o concepto.
    """

    _load()

    words = query.lower().split()

    matches = []

    for key, value in memory.items():

        text = f"{key} {value}".lower()

        for word in words:

            if word in text:

                matches.append(
                    f"{key}: {value}"
                )

                break

    if not matches:
        return "No encontré recuerdos relacionados."

    return "\n".join(matches)

_load()