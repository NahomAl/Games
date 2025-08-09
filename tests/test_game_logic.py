import unittest
from src.game_logic import TicTacToe


class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()

    def test_win_detection_rows(self):
        for row in range(3):
            self.game.reset()
            for col in range(3):
                self.game.board[row][col] = 'X'
            self.assertTrue(self.game.check_win('X'))

    def test_win_detection_columns(self):
        for col in range(3):
            self.game.reset()
            for row in range(3):
                self.game.board[row][col] = 'O'
            self.assertTrue(self.game.check_win('O'))

    def test_win_detection_diagonals(self):
        self.game.reset()
        for i in range(3):
            self.game.board[i][i] = 'X'
        self.assertTrue(self.game.check_win('X'))
        self.game.reset()
        for i in range(3):
            self.game.board[i][2-i] = 'O'
        self.assertTrue(self.game.check_win('O'))

    def test_draw_detection(self):
        self.game.board = [
            ['X', 'O', 'X'],
            ['X', 'O', 'O'],
            ['O', 'X', 'X']
        ]
        self.game.moves = 9
        self.assertTrue(self.game.is_draw())

    def test_valid_move_enforcement(self):
        self.assertTrue(self.game.make_move(0, 0))
        self.assertFalse(self.game.make_move(0, 0))
        self.assertTrue(self.game.make_move(0, 1))

    def test_ai_best_move(self):
        # Set up a board where AI (O) can win
        self.game.board = [
            ['O', 'O', ''],
            ['X', 'X', ''],
            ['', '', '']
        ]
        self.game.current_player = 'O'
        self.game.moves = 4
        move = self.game.minimax(True)[1]
        self.assertEqual(move, (0, 2))


if __name__ == '__main__':
    unittest.main()
