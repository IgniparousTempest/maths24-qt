import os

from PyQt5 import QtGui

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_icon(path: str):
    # print('Icons folder:', _ROOT)
    return os.path.join(_ROOT, path)


_difficulty_pixelmaps = {
    'easy': 'icon_difficulty_easy.svg',
    'medium': 'icon_difficulty_medium.svg',
    'hard': 'icon_difficulty_hard.svg'
}


def get_difficulty_pixelmap(difficulty: int) -> QtGui.QPixmap:
    def _lazy_return(difficulty_str: str) -> QtGui.QPixmap:
        if type(_difficulty_pixelmaps[difficulty_str]) == str:
            _difficulty_pixelmaps[difficulty_str] = QtGui.QPixmap(get_icon(_difficulty_pixelmaps[difficulty_str]))
        return _difficulty_pixelmaps[difficulty_str]

    if difficulty == 1:
        return _lazy_return('easy')
    if difficulty == 2:
        return _lazy_return('medium')
    else:
        return _lazy_return('hard')