import random
from dataclasses import dataclass
from fractions import Fraction as frac
from typing import List, Optional, Tuple

from maths24.error import AlreadySolved


@dataclass
class GameModel:
    """Class for keeping track of an item in inventory."""
    numbers: List[Optional[str]]

    def is_last_tile(self) -> bool:
        return self.numbers.count(None) >= 3

    def last_tile_id(self) -> int:
        for i in range(len(self.numbers)):
            if self.numbers[i] is not None:
                return i
        raise AlreadySolved("All tiles have been cleared")

    def make_move(self, index_remove: int, index_new: int, value: str) -> "GameModel":
        numbers = self.numbers[:]
        numbers[index_remove] = None
        numbers[index_new] = value
        return GameModel(numbers=numbers)

    @classmethod
    def evaluate(cls, number1: str, operation: str, number2: str) -> str:
        a = frac(number1)
        b = frac(number2)
        if operation == '+':
            return str(a + b)
        elif operation == '-':
            return str(a - b)
        elif operation == 'x':
            return str(a * b)
        else:
            return str(a / b)

    @classmethod
    def is_division(cls, operation: str) -> bool:
        return operation == '÷'

    @classmethod
    def random_puzzle(cls) -> "GameModel":
        """Generates a random game."""
        try:
            numbers = ['24']
            for _ in range(3):
                operation = random.choice(['+', '-', 'x', '÷'])
                num_a = str(random.randint(1, 13))
                index = random.randint(0, len(numbers) - 1)
                num_b = numbers[index]
                numbers[index] = GameModel.evaluate(num_a, operation, num_b)
                numbers.append(num_a)
            # Is a good puzzle?
            for num in numbers:
                # Must be an int in range
                num = frac(num)
                if not (frac(1) <= num <= frac(13) and str(num).isdigit()):
                    raise AssertionError('Ugly puzzle')
            return GameModel(numbers=[str(int(num)) for num in numbers])
        except (ZeroDivisionError, AssertionError):
            return cls.random_puzzle()

    def clue(self) -> Tuple[bool, str]:
        """
        Gets a clue to progress the puzzle.
        :return: A tuple of (can the puzzle be solved, next step string)
        """
        if self.is_last_tile():
            return self.numbers[self.last_tile_id()] == '24', ''

        for i, num_a in enumerate(self.numbers):
            if num_a is None:
                continue
            for j, num_b in enumerate(self.numbers):
                if num_b is None or i == j:
                    continue
                # Operations are in order of the difficulty humans find to do them
                for operation in ['+', '-', 'x', '÷']:
                    # Don't suggest negative number tiles
                    if operation == '-' and frac(num_a) < frac(num_b):
                        continue  # TODO: These operations are commutable, so this shouldn't be an error. I think?
                    # Check if this branch leads to a solution
                    try:
                        result = self.evaluate(num_a, operation, num_b)
                        solvable, _ = self.make_move(i, j, result).clue()
                        if solvable:
                            return True, f'{num_a} {operation} {num_b}'
                    except ZeroDivisionError:
                        pass
        return False, ''

    def solutions(self) -> List[str]:
        return [solution for solution in self._solutions()]

    def _solutions(self):
        for i, num_a in enumerate(self.numbers):
            if num_a is None:
                continue
            for j, num_b in enumerate(self.numbers):
                if num_b is None or i == j:
                    continue
                # Operations are in order of the difficulty humans find to do them
                for operation in ['+', '-', 'x', '÷']:
                    # Don't suggest negative number tiles
                    if operation == '-' and frac(num_a) < frac(num_b):
                        continue  # TODO: These operations are commutable, so this shouldn't be an error. I think?
                    # Check if this branch leads to a solution
                    try:
                        result = self.evaluate(num_a, operation, num_b)
                        model = self.make_move(i, j, result)
                        if model.is_last_tile() and model.numbers[model.last_tile_id()] == '24':
                            yield f'{num_a} {operation} {num_b}'
                        else:
                            for solution in model._solutions():
                                yield f'{num_a} {operation} ({solution})'
                    except ZeroDivisionError:
                        pass
        return []

    def difficulty(self) -> int:
        """
        Determines the difficulty of the puzzle.

        A puzzle is determined to be:
        - Easy if it has at least one solution that is comprised of only addition and subtraction.
        - Medium if at least one solution does not contain a divide.
        - Hard if all solutions contain divides.

        :return: The difficulty as an integer. 1 = easy, 2 = medium, 3 = hard, and -1 means unsolvable.
        """
        solutions = self.solutions()
        divides = 0
        for solution in solutions:
            if 'x' not in solution and '÷' not in solution:
                return 1
            elif '÷' in solution:
                divides += 1
        if divides == len(solutions):
            return 3
        else:
            return 2
