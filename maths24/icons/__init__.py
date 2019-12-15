import os

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_icon(path: str):
    # print('Icons folder:', _ROOT)
    return os.path.join(_ROOT, path)
