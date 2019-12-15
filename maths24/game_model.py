from dataclasses import dataclass
from typing import List, Optional


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
        raise RuntimeError("All tiles have been cleared")

    def make_move(self, index_remove: int, index_new: int, value: str) -> "GameModel":
        numbers = self.numbers[:]
        numbers[index_remove] = None
        numbers[index_new] = value
        return GameModel(numbers=numbers)

    @classmethod
    def evaluate(cls, number1: str, operation: str, number2: str) -> str:
        a = int(number1)
        b = int(number2)
        if operation == '+':
            return str(a + b)
        elif operation == '-':
            return str(a - b)
        elif operation == 'x':
            return str(a * b)
        else:
            return str(a // b)  # TODO: Fractions

    @classmethod
    def is_division(cls, operation: str) -> bool:
        return operation == '÷'

    @classmethod
    def random_puzzle(cls) -> "GameModel":
        """Generates a random game."""
        try:
            import random

            multiply = lambda a, b: a * b
            divide = lambda a, b: a / b
            add = lambda a, b: a + b
            subtract = lambda a, b: a - b

            numbers = [24]
            for _ in range(3):
                operation = random.choice([multiply, divide, add, subtract])
                num_a = random.randint(1, 13)
                index = random.randint(0, len(numbers) - 1)
                num_b = numbers[index]
                numbers[index] = operation(num_a, num_b)
                numbers.append(num_a)
            # Is a good puzzle?
            for num in numbers:
                # Must be an int in range
                if not (1 <= num <= 13 and (type(num) == int or num.is_integer())):
                    raise AssertionError('Ugly puzzle')
            return GameModel(numbers=[str(int(num)) for num in numbers])
        except (ZeroDivisionError, AssertionError):
            return cls.random_puzzle()
