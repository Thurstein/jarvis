import memory.long_term as long_term

workspace = {}


def set(key: str, value):

    workspace[key] = value


def get(key: str, default=None):

    return workspace.get(key, default)


def has(key: str) -> bool:
    """
    Indica si una clave existe en el workspace.
    """

    return key in workspace


def remove(key: str):
    """
    Elimina una clave del workspace si existe.
    """

    workspace.pop(key, None)


def keys():
    """
    Devuelve una lista con todas las claves almacenadas.
    """

    return list(workspace.keys())


def clear():

    workspace.clear()


def items():
    """
    Devuelve una copia de todos los elementos del workspace.
    """

    return dict(workspace)


def dump() -> str:
    """
    Devuelve una representación legible del contenido
    actual del workspace.
    """

    if not workspace:
        return "(vacío)"

    lines = []

    for key, value in workspace.items():
        lines.append(f"{key}: {value}")

    return "\n".join(lines)


def remember(key: str, value):
    """
    Guarda un dato en la memoria permanente.
    """

    return long_term.remember(key, value)


def recall(key: str, default=None):
    """
    Recupera un dato de la memoria permanente.
    """

    return long_term.recall(key, default)


def forget(key: str):
    """
    Elimina un dato de la memoria permanente.
    """

    return long_term.forget(key)