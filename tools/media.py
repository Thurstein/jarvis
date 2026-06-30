import keyboard
import time


def play_pause() -> str:
    """
    Reproduce o pausa la reproducción multimedia.
    """

    keyboard.send("play/pause media")

    return "Se cambió el estado de reproducción."


def next_track(count: int = 1) -> str:
    """
    Avanza una o más pistas.

    Args:
        count: cantidad de pistas.
    """

    count = max(1, int(count))

    for _ in range(count):
        keyboard.send("next track")
        time.sleep(0.1)

    return f"Se avanzó {count} pista(s)."


def previous_track(count: int = 1) -> str:
    """
    Retrocede una o más pistas.

    Args:
        count: cantidad de pistas.
    """

    count = max(1, int(count))

    for _ in range(count):
        keyboard.send("previous track")
        time.sleep(0.1)

    return f"Se retrocedió {count} pista(s)."


def stop_media() -> str:
    """
    Detiene la reproducción multimedia.
    """

    keyboard.send("stop media")

    return "La reproducción se detuvo."