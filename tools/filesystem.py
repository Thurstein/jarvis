from pathlib import Path
from memory import workspace
import subprocess
import os

SEARCH_ROOTS = [
    Path.home() / "Music",
    Path.home() / "Pictures",
    Path.home() / "Videos",
    Path.home() / "Documents",
    Path.home() / "Desktop",
    Path.home() / "Downloads",
]

def _iter_filesystem():

    for root in SEARCH_ROOTS:

        if not root.exists():
            continue

        yield from root.rglob("*")

def find_file(name: str) -> str:
    """
    Busca uno o más archivos por nombre en el computador.
    Devuelve la ruta completa de los archivos encontrados.
    """

    name = name.lower()

    search_name = Path(name).stem.lower()

    matches = []

    for file in _iter_filesystem():

        if not file.is_file():
            continue

        if search_name in file.stem.lower():

            matches.append(file)

            if len(matches) >= 10:
                break

    if not matches:
        return "No encontré ningún archivo."

    if len(matches) == 1:

        workspace.set(
            "last_file",
            str(matches[0])
        )

        return str(matches[0])

    workspace.set(
        "last_search",
        [str(f) for f in matches]
    )

    return "\n".join(str(f) for f in matches)

def _normalize_name(name: str) -> str:

    return (
        name.lower()
            .replace(" ", "")
            .replace("_", "")
            .replace("-", "")
    )

def open_file(path: str) -> str:
    """
    Abre un archivo utilizando la aplicación predeterminada de Windows.
    Si el nombre no coincide exactamente, intenta encontrar una coincidencia
    ignorando espacios, guiones y mayúsculas.
    """

    p = Path(path)

    # Si el usuario dice "ábrelo", "ese", etc.
    if path.lower() in {
        "lo",
        "ábrelo",
        "abrirlo",
        "ese",
        "ese archivo"
    }:

        last_file = workspace.get("last_file")

        if last_file:

            p = Path(last_file)

    # Si solo recibimos un nombre de archivo, buscarlo primero
    if not p.exists() and p.parent == Path("."):

        result = find_file(p.name)

        if result.startswith("No encontré"):
            return result

        if "\n" in result:
            return (
                "Encontré varios archivos:\n"
                + result
            )

        p = Path(result)

    # Caso 1: existe exactamente
    if p.exists() and p.is_file():
        os.startfile(str(p))
        return f"Archivo abierto: {p.name}"

    # Si la carpeta no existe, no podemos buscar
    if not p.parent.exists():
        return "La carpeta indicada no existe."

    target = _normalize_name(p.name)

    # Buscar coincidencia aproximada
    for file in p.parent.iterdir():

        if not file.is_file():
            continue

        if _normalize_name(file.name) == target:

            os.startfile(str(file))
            return f"Archivo abierto: {file.name}"

    return "El archivo no existe."

def _find_directory(name: str):

    name = name.lower().strip()

    # Carpetas principales del perfil de Windows
    known_folders = {
        "music": Path.home() / "Music",
        "música": Path.home() / "Music",
        "musica": Path.home() / "Music",

        "documents": Path.home() / "Documents",
        "documentos": Path.home() / "Documents",

        "downloads": Path.home() / "Downloads",
        "descargas": Path.home() / "Downloads",

        "desktop": Path.home() / "Desktop",
        "escritorio": Path.home() / "Desktop",

        "pictures": Path.home() / "Pictures",
        "imágenes": Path.home() / "Pictures",
        "imagenes": Path.home() / "Pictures",

        "videos": Path.home() / "Videos",
        "vídeos": Path.home() / "Videos",
    }

    if name in known_folders:

        folder = known_folders[name]

        if folder.exists():
            return [folder]

    matches = []

    for root in SEARCH_ROOTS:

        if not root.exists():
            continue

        for folder in root.rglob("*"):

            try:

                if not folder.is_dir():
                    continue

                # Ignorar junctions (Mi música, Mis imágenes, etc.)
                if os.path.isjunction(folder):
                    continue

                # Ignorar carpetas ocultas
                if folder.stat().st_file_attributes & 0x2:
                    continue

                if name in folder.name.lower():

                    matches.append(folder)

                    if len(matches) >= 10:
                        return matches

            except (PermissionError, OSError):
                continue

    return matches


def open_in_explorer(path: str) -> str:
    """
    Abre una carpeta en el Explorador de Windows.
    Si no recibe una ruta válida, intenta localizar una carpeta por nombre.
    """

    p = Path(path)

    # Si la ruta no existe, intentar buscar dentro del último directorio abierto
    if not p.exists():

        last_directory = workspace.get("last_directory")

        if last_directory:

            candidate = Path(last_directory) / path

            if candidate.exists() and candidate.is_dir():

                subprocess.Popen(["explorer", str(candidate)])

                workspace.set(
                    "last_directory",
                    str(candidate)
                )

                return f"Carpeta abierta: {candidate}"

    if p.exists():

        subprocess.Popen(["explorer", str(p)])

        workspace.set(
            "last_directory",
            str(p)
        )

        return f"Carpeta abierta: {p}"

    matches = _find_directory(path)

    if not matches:
        return "No encontré ninguna carpeta con ese nombre."

    if len(matches) > 1:

        return (
            "Encontré varias carpetas:\n"
            + "\n".join(str(m) for m in matches)
        )

    subprocess.Popen(["explorer", str(matches[0])])

    workspace.set(
        "last_directory",
        str(matches[0])
    )

    return f"Carpeta abierta: {matches[0]}"