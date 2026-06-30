workspace = {}


def set(key: str, value):

    workspace[key] = value


def get(key: str, default=None):

    return workspace.get(key, default)


def clear():

    workspace.clear()