from typing import List

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStyle
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from maths24.strings import Strings


# Create a subclass of QMainWindow to setup the calculator's GUI
class GameView(QMainWindow):
    """PyCalc's View (GUI)."""

    def __init__(self, strings: Strings):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self._strings = strings
        self.setWindowTitle('Maths 24')
        self.setFixedSize(235, 235)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the buttons
        self._create_undo_button()
        self._create_number_buttons()
        self._create_arithmetic_buttons()

    def _create_undo_button(self):
        self.undo_button = QPushButton('Undo')
        self.undo_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogBack')))
        self.generalLayout.addWidget(self.undo_button)

    def _create_number_buttons(self):
        """Create the buttons."""
        self.number_buttons = []
        buttons_layout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = [
            ('1', (0, 0)),
            ('2', (0, 1)),
            ('4', (1, 0)),
            ('12', (1, 1))
        ]
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons:
            button = QPushButton(btnText)
            button.setFixedSize(40, 40)
            buttons_layout.addWidget(button, pos[0], pos[1])
            self.number_buttons.append(button)
            # Add buttons_layout to the general layout
            self.generalLayout.addLayout(buttons_layout)

    def _create_arithmetic_buttons(self):
        """Create the arithmetic buttons."""
        self.arithmetic_buttons = {}
        layout = QHBoxLayout()
        # Button text | position on the QGridLayout
        buttons = ['+', '-', 'x', '÷']
        # Create the buttons and add them to the grid layout
        for btnText in buttons:
            self.arithmetic_buttons[btnText] = QPushButton(btnText)
            self.arithmetic_buttons[btnText].setFixedSize(40, 40)
            layout.addWidget(self.arithmetic_buttons[btnText])
            # Add buttonsLayout to the general layout
            self.generalLayout.addLayout(layout)

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
        for _, btn in self.arithmetic_buttons.items():
            btn.setStyleSheet("")

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
        for symbol, btn in self.arithmetic_buttons.items():
            if symbol == operation:
                btn.setStyleSheet("QPushButton { background-color: orange }")
            else:
                btn.setStyleSheet("")

    def perform_operation(self, button_first: int, button_second: int, result: str):
        """Performs calculation and updates buttons"""
        self.number_buttons[button_first].setVisible(False)
        self.number_buttons[button_second].setText(result)