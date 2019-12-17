from functools import partial
from typing import List, Optional

from maths24.dialogue_game_won import GameWonDialog
from maths24.dialogue_info import InfoDialog
from maths24.game_model import GameModel
from maths24.game_view import GameView
from maths24.strings import Strings


class GameController:
    """Game Controller class. Connects the GUI with the model."""

    def __init__(self, model: GameModel, view: GameView, strings: Strings):
        """Controller initializer."""
        self._view = view
        self._strings = strings

        self._connect_signals()  # Connect signals and slots

        self._new_game(model)

    def _new_game(self, model: GameModel, history: List[GameModel] = None):
        """Starts a new game with the provided model."""
        print(f'Starting a new game with:', model.numbers)
        self._model = model
        self._model_history: List[GameModel] = [model] if history is None else history

        self._selected_first_number_button_id: Optional[int] = None
        self._selected_operation: Optional[str] = None

        self._view.reset_display(model.numbers, self._model_history[0].difficulty())

    def _click_number(self, button_id: int):
        """

        :param button_id:
        """
        number = self._view.get_number(button_id)

        if button_id == self._selected_first_number_button_id:
            print('Can\'t select the same number button.')
            return
        elif self._selected_operation is not None:
            number_first = self._view.get_number(self._selected_first_number_button_id)
            operation = self._selected_operation

            if self._model.is_division(operation) and number == '0':
                print('Can\'t divide by zero.')
                return

            print(f'Evaluating {number_first} {operation} {number}')
            result = self._model.evaluate(number_first, operation, number)
            print(f'Result {number_first} {operation} {number} = {result}')
            self._view.perform_operation(self._selected_first_number_button_id, button_id, result)
            new_state = self._model_history[-1].make_move(self._selected_first_number_button_id, button_id, result)
            self._model_history.append(new_state)
            self._selected_operation = None
            self._view.set_operation_button(None)
        else:
            print(f'Expression is now {number} ? ?')
        self._selected_first_number_button_id = button_id
        self._view.set_number_button(button_id)

        # Is there one number button left?
        if self._model_history[-1].is_last_tile():
            index = self._model_history[-1].last_tile_id()
            number = self._view.get_number(index)
            has_won = number == '24'
            print(f'Game is {"won" if has_won else "lost"}, last tile is: {number}')
            if has_won:
                dlg = GameWonDialog(self._strings, parent=self._view)
                dlg.exec_()
                if dlg.should_next_game():
                    print('New game requested')
                    self._new_game(GameModel.random_puzzle())
                elif dlg.should_quit():
                    print('User is done :(')

            else:
                self._view.set_button_lost(index)

    def _click_operation(self, operation: str):
        """

        :param operation:
        """

        if self._selected_first_number_button_id is not None:
            number_first = self._view.get_number(self._selected_first_number_button_id)
            self._selected_operation = operation
            self._view.set_operation_button(operation)
            print(f'Expression is now {number_first} {operation} ?')

    def _click_undo(self):
        if len(self._model_history) > 1:
            self._new_game(self._model_history[-2], self._model_history[:-1])

    def _click_info(self):
        dlg = InfoDialog(self._strings, parent=self._view)
        dlg.exec_()

    def _click_skip(self):
        print('Skipping puzzle')
        self._new_game(GameModel.random_puzzle())

    def _click_hint(self):
        is_solvable, hint = self._model_history[-1].clue()
        print('Getting a hint:', hint if is_solvable else 'not solvable')
        if is_solvable:
            self._view.show_hint(hint)
        else:
            self._view.show_hint('This puzzle can not be solved, try pressing undo.')

    def _connect_signals(self):
        """Connect signals and slots."""
        for i, btn in enumerate(self._view.number_buttons):
            btn.clicked.connect(partial(self._click_number, i))

        for operation, btn in self._view.arithmetic_buttons.items():
            btn.clicked.connect(partial(self._click_operation, operation))

        self._view.pushButton_undo.clicked.connect(self._click_undo)
        self._view.pushButton_info.clicked.connect(self._click_info)
        self._view.pushButton_skip.clicked.connect(self._click_skip)
        self._view.pushButton_hint.clicked.connect(self._click_hint)
