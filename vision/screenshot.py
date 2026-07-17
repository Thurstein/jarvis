from pathlib import Path

import pyautogui

def get_last_screenshot() -> str:
    """
    Devuelve la ruta de la última captura.
    """

    image_path = (
        Path.home()
        / "Documents"
        / "Jarvis Screenshots"
        / "screenshot.png"
    )

    if not image_path.exists():
        return "No existe ninguna captura."

    return str(image_path)

def take_screenshot() -> str:
    """
    Captura la pantalla completa y guarda la imagen.
    """

    screenshots_dir = (
        Path.home()
        / "Documents"
        / "Jarvis Screenshots"
    )

    screenshots_dir.mkdir(
        exist_ok=True
    )

    image_path = (
        screenshots_dir
        / "screenshot.png"
    )

    pyautogui.screenshot(
        str(image_path)
    )

    return str(image_path)