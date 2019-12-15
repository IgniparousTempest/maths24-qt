from dataclasses import dataclass
from typing import List

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QSizePolicy

import maths24.maths24_ui
from maths24 import icons
from maths24.strings import Strings


@dataclass
class _State:
    unselected: QtGui.QIcon
    selected: QtGui.QIcon

    def from_paths(self):
        return _State(
            unselected=QtGui.QIcon(QtGui.QPixmap(self.unselected)),
            selected=QtGui.QIcon(QtGui.QPixmap(self.selected))
        )


_icons = {
    '+': _State(
        unselected=icons.get_icon('icon_plus.svg'),
        selected=icons.get_icon('icon_plus_selected.svg')
    ),
    '-': _State(
        unselected=icons.get_icon('icon_minus.svg'),
        selected=icons.get_icon('icon_minus_selected.svg')
    ),
    'x': _State(
        unselected=icons.get_icon('icon_multiply.svg'),
        selected=icons.get_icon('icon_multiply_selected.svg')
    ),
    '÷': _State(
        unselected=icons.get_icon('icon_divide.svg'),
        selected=icons.get_icon('icon_divide_selected.svg')
    )
}


class GameView(QtWidgets.QMainWindow, maths24.maths24_ui.Ui_MainWindow):
    def __init__(self, strings: Strings, parent=None):
        super(GameView, self).__init__(parent)
        self.setupUi(self)

        # Set icons to absolute path, necessary for deb
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icons.get_icon('icon.svg'))))
        self.pushButton_info.setIcon(QtGui.QIcon(QtGui.QPixmap(icons.get_icon('icon_info.svg'))))
        self.pushButton_hint.setIcon(QtGui.QIcon(QtGui.QPixmap(icons.get_icon('icon_bulb.svg'))))
        self.pushButton_skip.setIcon(QtGui.QIcon(QtGui.QPixmap(icons.get_icon('icon_next.svg'))))
        self.pushButton_undo.setIcon(QtGui.QIcon(QtGui.QPixmap(icons.get_icon('icon_undo.svg'))))

        self.number_buttons = [self.pushButton_number_1, self.pushButton_number_2, self.pushButton_number_3, self.pushButton_number_4]

        self.arithmetic_buttons = {
            '+': self.pushButton_addition,
            '-': self.pushButton_subtraction,
            'x': self.pushButton_multiplication,
            '÷': self.pushButton_division
        }
        for symbol, state in _icons.items():
            _icons[symbol] = _icons[symbol].from_paths()

        self._set_size_policies()

    def _set_size_policies(self):
        for btn in self.number_buttons:
            policy = btn.sizePolicy()
            policy.setRetainSizeWhenHidden(True)  # Does not disappear when hidden
            btn.setSizePolicy(policy)

    def reset_display(self, numbers: List[str]):
        """Resets the display for a new game."""
        # Reset number buttons
        for i, btn in enumerate(self.number_buttons):
            if numbers[i] is not None:
                btn.setText(numbers[i])
                btn.setVisible(True)
                btn.setStyleSheet("")
            else:
                btn.setVisible(False)

        # Reset symbol buttons
        for symbol, btn in self.arithmetic_buttons.items():
            btn.setIcon(_icons[symbol].unselected)
            # btn.setStyleSheet("")

    def get_number(self, index: int):
        return self.number_buttons[index].text()

    def set_number_button(self, index: int):
        for i, btn in enumerate(self.number_buttons):
            if i == index:
                btn.setStyleSheet("QPushButton { background-color: green }")
            else:
                btn.setStyleSheet("")

    def set_button_lost(self, index: int):
        self.number_buttons[index].setStyleSheet("QPushButton { background-color: red }")

    def set_operation_button(self, operation: str):
        print(operation)
        for symbol, btn in self.arithmetic_buttons.items():
            if symbol == operation:
                btn.setIcon(_icons[symbol].selected)
                # btn.setStyleSheet("QPushButton { background-color: orange }")
            else:
                btn.setIcon(_icons[symbol].unselected)
                # btn.setStyleSheet("")

    def perform_operation(self, button_first: int, button_second: int, result: str):
        """Performs calculation and updates buttons"""
        self.number_buttons[button_first].setVisible(False)
        self.number_buttons[button_second].setText(result)