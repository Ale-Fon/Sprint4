import unittest
from game_logic import GeneralGame, cpuPlayer

class TestGeneralGameCPU(unittest.TestCase):

    def test_general_game_cpu_vs_cpu(self):
        game = GeneralGame(5)
        blue_cpu = cpuPlayer("Blue")
        red_cpu = cpuPlayer("Red")

        while not game.is_full():
            current_cpu = blue_cpu if game.current_turn == "Blue" else red_cpu
            row, col = current_cpu.choose_position(game)
            letter = current_cpu.choose_letter()
            _, sosLine = game.letterPlace(row, col, letter)

            if not sosLine:
                game.switch_turn()

        result = game.checkWinnerScore()
        self.assertIn(result, ["Blue", "Red", "Draw"])

if __name__ == "__main__":
    unittest.main()