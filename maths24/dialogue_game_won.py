import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout

from maths24.strings import Strings


class GameWonDialog(QDialog):

    def __init__(self, strings: Strings, parent=None):
        """Initializer."""
        super().__init__(parent)
        self._shouldQuit = False
        self._shouldNextPuzzle = False
        self.setWindowTitle('You won!')
        dlgLayout = QVBoxLayout()

        label = QLabel()
        label.setText('You have made 24 and won!')
        dlgLayout.addWidget(label)

        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        btns.button(QDialogButtonBox.Apply).setText('Next Puzzle')
        btns.button(QDialogButtonBox.Cancel).setText('Quit')
        btns.button(QDialogButtonBox.Apply).clicked.connect(self.on_next_puzzle)
        btns.button(QDialogButtonBox.Cancel).clicked.connect(self.on_quit)
        dlgLayout.addWidget(btns)

        self.setLayout(dlgLayout)

    def on_next_puzzle(self):
        self._shouldNextPuzzle = True
        self.close()

    def on_quit(self):
        self._shouldQuit = True
        self.close()

    def should_next_game(self):
        """User has requested a new game."""
        return self._shouldNextPuzzle

    def should_quit(self):
        """User has requested the game should end."""
        return self._shouldQuit


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = GameWonDialog(Strings('en'))
    dlg.show()
    sys.exit(app.exec_())
