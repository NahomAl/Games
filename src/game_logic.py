"""
Tic-Tac-Toe game logic module.
Implements board state, win/draw detection, move validation, and unbeatable AI (minimax).
"""
from typing import List, Optional, Tuple
import random


class TicTacToe:
    def __init__(self):
        self.reset()
        self.scores = {'X': 0, 'O': 0}

    def reset(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.moves = 0
        self.game_over = False

    def make_move(self, row: int, col: int) -> bool:
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            self.moves += 1
            if self.check_win(self.current_player):
                self.winner = self.current_player
                self.scores[self.current_player] += 1
                self.game_over = True
            elif self.moves == 9:
                self.winner = None
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_win(self, player: str) -> bool:
        b = self.board
        # Rows, columns, diagonals
        for i in range(3):
            if all(b[i][j] == player for j in range(3)):
                return True
            if all(b[j][i] == player for j in range(3)):
                return True
        if all(b[i][i] == player for i in range(3)):
            return True
        if all(b[i][2-i] == player for i in range(3)):
            return True
        return False

    def get_winning_combination(self, player: str) -> Optional[List[Tuple[int, int]]]:
        b = self.board
        for i in range(3):
            if all(b[i][j] == player for j in range(3)):
                return [(i, j) for j in range(3)]
            if all(b[j][i] == player for j in range(3)):
                return [(j, i) for j in range(3)]
        if all(b[i][i] == player for i in range(3)):
            return [(i, i) for i in range(3)]
        if all(b[i][2-i] == player for i in range(3)):
            return [(i, 2-i) for i in range(3)]
        return None

    def is_draw(self) -> bool:
        return self.moves == 9 and self.winner is None

    def valid_moves(self) -> List[Tuple[int, int]]:
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']

    def minimax(self, is_max: bool) -> Tuple[int, Optional[Tuple[int, int]]]:
        if self.check_win('O'):
            return (1, None)
        if self.check_win('X'):
            return (-1, None)
        if self.is_draw():
            return (0, None)
        best = (-2, None) if is_max else (2, None)
        for (i, j) in self.valid_moves():
            self.board[i][j] = 'O' if is_max else 'X'
            self.moves += 1
            score, _ = self.minimax(not is_max)
            self.board[i][j] = ''
            self.moves -= 1
            if is_max:
                if score > best[0]:
                    best = (score, (i, j))
            else:
                if score < best[0]:
                    best = (score, (i, j))
        return best

    def ai_move(self) -> Optional[Tuple[int, int]]:
        if self.game_over:
            return None
        _, move = self.minimax(self.current_player == 'O')
        if move:
            self.make_move(*move)
        return move

    def set_starting_player(self, player: str):
        if player in ['X', 'O']:
            self.current_player = player

    def get_board(self) -> List[List[str]]:
        return [row[:] for row in self.board]

    def get_scores(self) -> dict:
        return self.scores.copy()
