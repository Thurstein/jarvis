from pathlib import Path
from memory import workspace
import subprocess
import unicodedata
import os

SEARCH_ROOTS = [
    Path.home() / "Music",
    Path.home() / "Pictures",
    Path.home() / "Videos",
    Path.home() / "Documents",
    Path.home() / "Desktop",
    Path.home() / "Downloads",
]

KNOWN_FOLDERS = {
    "music": Path.home() / "Music",
    "musica": Path.home() / "Music",

    "documents": Path.home() / "Documents",
    "documentos": Path.home() / "Documents",

    "downloads": Path.home() / "Downloads",
    "descargas": Path.home() / "Downloads",

    "desktop": Path.home() / "Desktop",
    "escritorio": Path.home() / "Desktop",

    "pictures": Path.home() / "Pictures",
    "imagenes": Path.home() / "Pictures",

    "videos": Path.home() / "Videos",
    "videos": Path.home() / "Videos",
}

def _iter_filesystem(files=True, directories=True):
    """
    Recorre el sistema de archivos devolviendo archivos,
    carpetas o ambos según los parámetros.
    """

    for root in SEARCH_ROOTS:

        if not root.exists():
            continue

        for item in root.rglob("*"):

            try:

                if item.is_file() and files:
                    yield item

                elif item.is_dir() and directories:
                    yield item

            except (PermissionError, OSError):
                continue

def find_file(name: str) -> str:
    """
    Busca uno o más archivos por nombre en el computador.
    Devuelve la ruta completa de los archivos encontrados.
    """

    name = _clean_text(name)
    matches = []

    for file in _iter_filesystem(files=True, directories=False):

        if name in _clean_text(file.name):

            matches.append(file)

            if len(matches) >= 10:
                break

    # Eliminar duplicados conservando el orden
    matches = list(dict.fromkeys(matches))

    if not matches:
        return "No encontré ningún archivo."

    if len(matches) == 1:
        return str(matches[0])

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

        workspace.set("last_file", str(p))

        suffix = p.suffix.lower()

        if suffix == ".mp3":
            workspace.set("last_song", str(p))

        elif suffix == ".pdf":
            workspace.set("last_document", str(p))

        elif suffix in {".png", ".jpg", ".jpeg", ".webp"}:
            workspace.set("last_image", str(p))
        
        os.startfile(str(p))
        return f"Archivo abierto: {p.name}"

    # Si la carpeta no existe, no podemos buscar
    if not p.parent.exists():
        return "La carpeta indicada no existe."

    target = _normalize_name(
        _clean_text(p.name)
    )

    # Buscar coincidencia aproximada
    for file in p.parent.iterdir():

        if not file.is_file():
            continue

        if (
            _normalize_name(
                _clean_text(file.name)
            ) == target
        ):

            workspace.set("last_file", str(file))

            suffix = p.suffix.lower()

            if suffix == ".mp3":
                workspace.set("last_song", str(file))

            elif suffix == ".pdf":
                workspace.set("last_document", str(file))

            elif suffix in {".png", ".jpg", ".jpeg", ".webp"}:
                workspace.set("last_image", str(file))

            os.startfile(str(file))
            return f"Archivo abierto: {file.name}"

    return "El archivo no existe."

def _find_directory(name: str):

    name = _clean_text(name)

    # Si el modelo envía una ruta parcial, nos quedamos
    # solamente con el último directorio.
    name = _clean_text(Path(name).name)

    # Carpetas principales del perfil de Windows


    if name in KNOWN_FOLDERS:

        folder = KNOWN_FOLDERS[name]

        if folder.exists():
            return [folder]

    matches = []

    for folder in _iter_filesystem(
        files=False,
        directories=True
    ):

        try:

            # Ignorar junctions (Mi música, Mis imágenes, etc.)
            if os.path.isjunction(folder):
                continue

            # Ignorar carpetas ocultas
            if folder.stat().st_file_attributes & 0x2:
                continue

            if name in _clean_text(folder.name):

                matches.append(folder)

                if len(matches) >= 10:
                    return matches

        except (PermissionError, OSError):
            continue

    return matches

def _clean_text(text: str) -> str:
    """
    Normaliza un texto para facilitar búsquedas:
    - minúsculas
    - sin tildes
    - sin espacios al inicio/final
    """

    text = text.lower().strip()

    text = unicodedata.normalize("NFD", text)
    text = "".join(
        c for c in text
        if unicodedata.category(c) != "Mn"
    )

    return text

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

def create_text_file(
    filename: str,
    content: str
) -> str:
    """
    Crea un archivo de texto dentro de Documents.
    """

    documents = Path.home() / "Documents"

    file_path = documents / filename

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    workspace.set(
        "last_file",
        str(file_path)
    )

    return f"Archivo creado: {file_path}"

def append_text_file(path: str, content: str) -> str:
    """
    Agrega texto al final de un archivo.
    """

    p = Path(path)

    # Si el archivo no existe:
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

    if not p.exists():
        return "El archivo no existe."

    # Si el archivo existe:
    with open(p, "a", encoding="utf-8") as f:
        f.write("\n" + content)

    workspace.set("last_file", str(p))

    return f"Texto agregado al final del archivo: {p.name}"

def overwrite_text_file(path: str, content: str) -> str:
    """
    Reemplaza completamente el contenido
    de un archivo de texto.
    """
    p = Path(path)

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

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Archivo sobrescrito: {p.name}"

def read_text_file(path: str) -> str:
    """
    Lee el contenido de un archivo de texto.
    """

    p = Path(path)

    if path.lower() in {
        "lo",
        "léelo",
        "leelo",
        "ese archivo",
        "el archivo"
    }:

        last_file = workspace.get("last_file")

        if last_file:
            p = Path(last_file)

    if not p.exists():
        return "El archivo no existe."

    if not p.is_file():
        return "La ruta indicada no es un archivo."

    workspace.set(
        "last_file",
        str(p)
    )

    return p.read_text(
        encoding="utf-8"
    )