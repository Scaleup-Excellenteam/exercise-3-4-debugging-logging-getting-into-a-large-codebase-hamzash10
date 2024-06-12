import unittest
from unittest.mock import patch, Mock

import chess_engine
import Piece
from enums import Player


class MyTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
