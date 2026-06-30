import json
import shutil
import subprocess
from pathlib import Path


CONFIG_FILE = Path(__file__).parent.parent / "config" / "programs.json"


def load_programs():

    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def open_program(name: str) -> str:
    """
    Abre un programa instalado en el sistema.

    Args:
        name: nombre del programa.
    """

    programs = load_programs()

    key = name.lower().strip()

    # Primero buscamos en programs.json
    if key in programs:

        executable = programs[key]

        subprocess.Popen(executable)

        return f"Programa '{name}' abierto correctamente."

    # Si no existe, intentamos encontrarlo en el PATH
    executable = shutil.which(key)

    if executable:

        subprocess.Popen(executable)

        return f"Programa '{name}' abierto correctamente."

    return f"No encontré el programa '{name}'."