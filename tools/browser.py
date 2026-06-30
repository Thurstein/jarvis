import webbrowser


def open_url(url: str) -> str:
    """
    Abre una página web en el navegador predeterminado.

    Args:
        url: Dirección web.
    """

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    webbrowser.open(url)

    return f"Se abrió {url}"