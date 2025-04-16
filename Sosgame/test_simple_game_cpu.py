import unittest
from game_logic import SimpleGame, cpuPlayer

class TestSimpleGameCPU(unittest.TestCase):

    def test_simple_game_cpu_vs_cpu(self):
        game = SimpleGame(6)
        blue_cpu = cpuPlayer("Blue")
        red_cpu = cpuPlayer("Red")

        while not game.is_full():
            current_cpu = blue_cpu if game.current_turn == "Blue" else red_cpu
            row, col = current_cpu.choose_position(game)
            letter = current_cpu.choose_letter()
            winner, sosLine = game.letterPlace(row, col, letter)

            if winner:
                self.assertIn(winner, ["Blue", "Red"])
                return

            if not sosLine:
                game.switch_turn()

        self.assertTrue(game.is_full())

if __name__ == "__main__":
    unittest.main()