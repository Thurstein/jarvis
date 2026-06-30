from pathlib import Path
import subprocess


# Ruta al ejecutable nircmd.exe
NIRCMD = Path(__file__).parent.parent / "nircmd" / "nircmd.exe"


def set_volume(level: int) -> str:
    """
    Establece el volumen maestro de Windows.

    Args:
        level: volumen entre 0 y 100.
    """

    level = max(0, min(100, int(level)))

    # NirCmd usa un rango entre 0 y 65535
    volume = int(level / 100 * 65535)

    subprocess.run(
        [
            str(NIRCMD),
            "setsysvolume",
            str(volume)
        ],
        check=True
    )

    return f"Volumen ajustado al {level}%"