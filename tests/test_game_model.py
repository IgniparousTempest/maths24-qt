import random
import unittest

from maths24.error import AlreadySolved
from maths24.game_model import GameModel


class MyTestCase(unittest.TestCase):
    def test_clue(self):
        """
        Tests solving on random board states.
        :return:
        """
        for _ in range(1000):
            try:
                numbers=[str(random.randint(-13, 13)) for _ in range(4)]
                for i in [random.randint(0, 3) for _ in range(random.randint(0, 4))]:
                    numbers[i] = None
                model = GameModel(numbers=numbers)
                solvable, clue = model.clue()
                self.assertEqual(type(clue), str, 'Output should be a string.')
                self.assertEqual(type(solvable), bool, 'Solvable flag should be a bool.')
                if solvable:
                    self.assertGreater(len(clue), 0, 'Clue string should not be empty')
            except AlreadySolved as e:
                self.assertEqual(model.numbers, [None, None, None, None], 'Clue failed when not empty.')
                # self.fail(f"clue() raised {e} for {model}")

    def test_random_puzzle(self):
        """
        Generates some random puzzles.
        :return:
        """
        for _ in range(1000):
            model = GameModel.random_puzzle()
            self.assertEqual([type(i) for i in model.numbers], [str, str, str, str], 'Model should be number strings')

    def test_integration_puzzle_generation_and_solving(self):
        """
        Generates some random puzzles and solves them.
        Ensures all generated puzzles are solvable.
        :return:
        """
        for _ in range(1000):
            model = GameModel.random_puzzle()
            solvable, clue = model.clue()
            self.assertTrue(solvable, f'Generated puzzle ({model.numbers}) must be solvable')
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
