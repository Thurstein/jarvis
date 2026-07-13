from pathlib import Path
import json
import unicodedata

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

def normalize(text: str) -> str:

    return "".join(
        c for c in unicodedata.normalize(
            "NFD",
            text
        )
        if unicodedata.category(c) != "Mn"
    ).lower()

def search_memory(query: str) -> str:
    """
    Busca recuerdos almacenados en la memoria.

    IMPORTANTE:

    - La información devuelta es la única fuente válida.
    - Nunca inventar, completar o inferir datos no presentes.
    - Nunca asumir gustos, preferencias o hechos a partir de recuerdos parciales.
    - Si un dato no aparece explícitamente en los resultados, se considera desconocido.
    - Responder únicamente usando la información devuelta.
    - Si devuelve "No encontré recuerdos relacionados.", significa que no existe información almacenada.
    """

    _load()

    words = (
        normalize(query)
        .replace("¿", "")
        .replace("?", "")
        .replace(",", "")
        .replace(".", "")
        .split()
    )

    matches = []
    scores = []

    for key, value in memory.items():

        text = normalize(
            f"{key} {value}"
        )

        text_words = text.replace("_", " ").split()

        # print(f"Key: {key}")
        # print(f"Text words: {text_words}")

        score = 0

        for word in words:

            if len(word) <= 3:
                continue

            for text_word in text_words:

                if word == text_word:
                    score += 3

                elif word in text_word or text_word in word:
                    score += 1

        if score > 0:
            print(f"Match: {key} | score={score}")

            if key.startswith("musica_playlist_"):
                score += 5

            matches.append(
                f"{key}: {value}"
            )

            scores.append(score)
    
    # print("\n[Memory search]")
    # print("Words:", words)
    # print("Matches:", matches)

    if not matches:
        return "No encontré recuerdos relacionados."

    matches = [
        item
        for _, item in sorted(
            zip(scores, matches),
            reverse=True
        )
    ]

    return "\n".join(matches[:6])

_load()