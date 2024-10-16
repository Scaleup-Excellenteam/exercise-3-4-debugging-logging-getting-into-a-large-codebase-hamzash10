import unittest
from unittest.mock import patch

import chess_engine
from enums import Player
from ai_engine import chess_ai

class integration_tests(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment before each test.

        This method initializes a new game state and a chess AI instance, and sets up
        an empty 8x8 chess board.
        """
        self.test_game_state = chess_engine.game_state()
        self.test_game_state.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]
        self.chess_ai = chess_ai()

    def test_knight_get_valid_piece_moves(self):
        """
        Test the knight piece's valid moves, including both peaceful moves and takes.

        This test sets up a knight on the board with two opponent pawns and verifies that the
        knight's valid moves include both peaceful moves and takes. It mocks the knight's
        'get_valid_peaceful_moves' and 'get_valid_piece_takes' methods to focus on the
        'get_valid_piece_moves' logic.

        Steps:
        1. Place a knight piece on the board at position (3, 4).
        2. Place two opponent pawns on the board at positions (1, 3) and (5, 5).
        3. Define the expected peaceful moves and takes.
        4. Mock the knight's 'get_valid_peaceful_moves' and 'get_valid_piece_takes' methods
           to return the expected peaceful moves and takes.
        5. Call the knight's 'get_valid_piece_moves' method to get the actual moves.
        6. Assert that the actual moves match the expected moves.
        """
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
        """
        Define a side effect function for mocking the 'get_piece_value' method of the chess AI.

        This function returns different values based on the type of piece and the player.
        - Knight: -30 for PLAYER_1, 30 for PLAYER_2
        - Pawn: 10 for PLAYER_1, -10 for PLAYER_2

        Args:
        evaluated_piece (Piece): The piece being evaluated.
        player (Player): The player owning the piece.

        Returns:
        int: The value of the piece.
        """
        if isinstance(evaluated_piece, chess_engine.Knight):
            return -30 if player == Player.PLAYER_1 else 30
        if isinstance(evaluated_piece, chess_engine.Pawn):
            return 10 if player == Player.PLAYER_1 else -10
        return 0

    def test_evaluate_board(self):
        """
        Test the chess AI's board evaluation function.

        This test sets up a knight and a pawn on the board and verifies that the AI correctly
        evaluates the board's value using a mocked 'get_piece_value' method.

        Steps:
        1. Place a knight piece on the board at position (3, 4).
        2. Place an opponent's pawn on the board at position (1, 3).
        3. Mock the chess AI's 'get_piece_value' method with the 'side_effect' function.
        4. Call the AI's 'evaluate_board' method to get the board's evaluation.
        5. Assert that the evaluation matches the expected value (-20).
        """
        board = self.test_game_state
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        board.board[3][4] = knight
        pawn1 = chess_engine.Pawn('p', 1, 3, Player.PLAYER_2)
        self.test_game_state.board[1][3] = pawn1

        with patch.object(chess_ai, 'get_piece_value', side_effect=self.side_effect):
            evaluation = self.chess_ai.evaluate_board(board, Player.PLAYER_1)
            self.assertEqual(evaluation, -20)


if __name__ == '__main__':
    unittest.main()