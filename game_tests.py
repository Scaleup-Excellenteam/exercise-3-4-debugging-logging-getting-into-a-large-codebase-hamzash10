import unittest
from unittest.mock import patch, Mock

import chess_engine
import Piece
from enums import Player
from ai_engine import chess_ai


class unit_tests(unittest.TestCase):

    def setUp(self):
        self.test_game_state = chess_engine.game_state()
        self.test_game_state.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]

    def test_knight_valid_piece_takes_1(self):
        with patch.object(chess_engine.game_state, 'is_valid_piece', return_value=False):
            board = self.test_game_state
            knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
            board.board[3][4] = knight
            expected_takes = []
            valid_takes = knight.get_valid_piece_takes(board)
            self.assertEqual(expected_takes, valid_takes)

    def test_knight_valid_peaceful_moves_1(self):
        with patch.object(chess_engine.game_state, 'is_valid_piece', return_value=False):
            board = self.test_game_state
            knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
            board.board[3][4] = knight
            expected_moves = {(5, 3), (5, 5), (4, 6), (4, 2), (2, 2), (2, 6), (1, 3), (1, 5)}
            valid_moves = set(knight.get_valid_peaceful_moves(board))
            self.assertEqual(expected_moves, valid_moves)

    def test_knight_valid_piece_takes_2(self):
        board = self.test_game_state
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        pawn = chess_engine.Pawn('p', 5, 3, Player.PLAYER_2)
        board.board[3][4] = knight
        board.board[5][3] = pawn
        expected_takes = [(5, 3)]
        valid_takes = knight.get_valid_piece_takes(board)
        self.assertEqual(expected_takes, valid_takes)

    def test_knight_valid_peaceful_moves_2(self):
        board = self.test_game_state
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        pawn = chess_engine.Pawn('p', 5, 3, Player.PLAYER_2)
        board.board[3][4] = knight
        board.board[5][3] = pawn
        expected_takes = {(5, 5), (4, 6), (4, 2), (2, 2), (2, 6), (1, 3), (1, 5)}
        valid_takes = set(knight.get_valid_peaceful_moves(board))
        self.assertEqual(expected_takes, valid_takes)

    def set_full_takes(self):
        board = self.test_game_state
        pawn1 = chess_engine.Pawn('p', 5, 3, Player.PLAYER_2)
        pawn2 = chess_engine.Pawn('p', 5, 5, Player.PLAYER_2)
        pawn3 = chess_engine.Pawn('p', 4, 2, Player.PLAYER_2)
        pawn4 = chess_engine.Pawn('p', 2, 2, Player.PLAYER_2)
        pawn5 = chess_engine.Pawn('p', 1, 3, Player.PLAYER_2)
        pawn6 = chess_engine.Pawn('p', 1, 5, Player.PLAYER_2)
        pawn7 = chess_engine.Pawn('p', 2, 6, Player.PLAYER_2)
        pawn8 = chess_engine.Pawn('p', 4, 6, Player.PLAYER_2)
        board.board[5][3] = pawn1
        board.board[5][5] = pawn2
        board.board[4][2] = pawn3
        board.board[2][2] = pawn4
        board.board[1][3] = pawn5
        board.board[1][5] = pawn6
        board.board[2][6] = pawn7
        board.board[4][6] = pawn8
        return board

    def test_knight_valid_piece_takes_3(self):
        board = self.set_full_takes()
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        board.board[3][4] = knight
        expected_takes = {(5, 3), (5, 5), (4, 2), (2, 2), (1, 3), (1, 5), (2, 6), (4, 6)}
        valid_takes = set(knight.get_valid_piece_takes(board))
        self.assertEqual(expected_takes, valid_takes)

    def test_knight_valid_peaceful_moves_3(self):
        board = self.set_full_takes()
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        board.board[3][4] = knight
        expected_takes = []
        valid_takes = knight.get_valid_peaceful_moves(board)
        self.assertEqual(expected_takes, valid_takes)


class integration_tests(unittest.TestCase):

    def setUp(self):
        self.test_game_state = chess_engine.game_state()
        self.test_game_state.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]
        self.chess_ai = chess_ai()

    def test_knight_get_valid_piece_moves(self):
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        self.test_game_state.board[3][4] = knight

        pawn1 = chess_engine.Pawn('p', 1, 3, Player.PLAYER_2)
        pawn2 = chess_engine.Pawn('p', 5, 5, Player.PLAYER_2)
        self.test_game_state.board[1][3] = pawn1
        self.test_game_state.board[5][5] = pawn2
        expected_peaceful_moves = [(1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 3)]
        expected_takes = [(1, 3), (5, 5)]
        expected_moves = expected_peaceful_moves + expected_takes

        # mocking the two functions to check only the logic of get_valid_piece_moves
        with patch.object(knight, 'get_valid_peaceful_moves', return_value=expected_peaceful_moves), \
                patch.object(knight, 'get_valid_piece_takes', return_value=expected_takes):
            valid_moves = knight.get_valid_piece_moves(self.test_game_state)
            self.assertEqual(set(valid_moves), set(expected_moves))

    def side_effect(self, evaluated_piece, player):
        if isinstance(evaluated_piece, chess_engine.Knight):
            return -30 if player == Player.PLAYER_1 else 30
        if isinstance(evaluated_piece, chess_engine.Pawn):
            return 10 if player == Player.PLAYER_1 else -10
        return 0

    def test_evaluate_board(self):
        board = self.test_game_state
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        board.board[3][4] = knight
        pawn1 = chess_engine.Pawn('p', 1, 3, Player.PLAYER_2)
        self.test_game_state.board[1][3] = pawn1

        with patch.object(chess_ai, 'get_piece_value', side_effect=self.side_effect):
            evaluation = self.chess_ai.evaluate_board(board, Player.PLAYER_1)
            self.assertEqual(evaluation, -20)


class system_tests(unittest.TestCase):
    def setUp(self):
        self.test_game_state = chess_engine.game_state()

    def test_full_game(self):
        board = self.test_game_state
        board.move_piece((1, 2), (2, 2), False)
        board.move_piece((6, 3), (4, 3), False)
        board.move_piece((1, 1), (3, 1), False)
        board.move_piece((7, 4), (3, 0), False)
        self.assertEqual(board.checkmate_stalemate_checker(), 0)


if __name__ == '__main__':
    unittest.main()
