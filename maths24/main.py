import locale
import sys

from PyQt5.QtWidgets import QApplication

from maths24.game_model import GameModel
from maths24.game_view import GameView
from maths24.game_controller import GameController
from maths24.strings import Strings

__version__ = '0.9.9'
__author__ = 'Courtney Richard Pitcher'


def get_language():
    return locale.getdefaultlocale()[0]


# Client code
def main():
    """Main function."""
    # Language settings
    print(f'System language is {get_language()}')
    strings = Strings(get_language())  # TODO: Checkout Qt Translate

    # Create an instance of QApplication
    game = QApplication(sys.argv)
    # Show the calculator's GUI
    model = GameModel.random_puzzle()
    view = GameView(strings)
    view.show()
    # Create instances of the model and the controller
    GameController(model=model, view=view, strings=strings)
    # Execute the calculator's main loop
    sys.exit(game.exec_())


if __name__ == '__main__':
    main()
