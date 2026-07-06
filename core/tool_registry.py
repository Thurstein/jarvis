from tools.filesystem import (
    find_file,
    open_file,
    open_in_explorer,
)

from tools.programs import open_program
from tools.browser import open_url
from tools.volume import set_volume

from tools.media import (
    play_pause,
    next_track,
    previous_track,
    stop_media,
)

from memory.long_term import (
    remember_text,
    recall_text,
)


def register_tools(assistant):
    """
    Registra todas las herramientas disponibles.
    """

    assistant.register_tools([
        open_program,
        open_url,
        set_volume,

        play_pause,
        next_track,
        previous_track,
        stop_media,

        find_file,
        open_file,
        open_in_explorer,

        remember_text,
        recall_text,
    ])