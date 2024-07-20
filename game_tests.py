import unittest
from unittest.mock import patch, Mock

import chess_engine
import Piece
from enums import Player
from ai_engine import chess_ai


class unit_tests(unittest.TestCase):

    def setUp(self):
        """
        Initialize an empty 8x8 chess board for testing purposes.
        This method is called before every test case.
        """
        self.test_game_state = chess_engine.game_state()
        self.test_game_state.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]

    def test_knight_valid_piece_takes_1(self):
        """
        Test the knight piece's valid take moves in a specific scenario.

        This test sets up a knight on the board and verifies that it has no valid piece
        takes when 'is_valid_piece' is mocked to always return False.

        Steps:
        1. Mock the 'is_valid_piece' method of the game state to always return False.
        2. Place a knight piece on the board at position (3, 4).
        3. Define the expected list of valid takes (which should be empty).
        4. Call the knight's 'get_valid_piece_takes' method to get the actual valid takes.
        5. Assert that the actual valid takes match the expected takes.
        """
        with patch.object(chess_engine.game_state, 'is_valid_piece', return_value=False):
            board = self.test_game_state
            knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
            board.board[3][4] = knight
            expected_takes = []
            valid_takes = knight.get_valid_piece_takes(board)
            self.assertEqual(expected_takes, valid_takes)

    def test_knight_valid_peaceful_moves_1(self):
        """
            Test the knight piece's valid peaceful moves in a specific scenario.

            This test sets up a knight on the board and verifies that it has the correct set of valid
            peaceful moves (i.e., moves that do not involve taking another piece) when 'is_valid_piece'
            is mocked to always return False.

            Steps:
            1. Mock the 'is_valid_piece' method of the game state to always return False.
            2. Place a knight piece on the board at position (3, 4).
            3. Define the expected set of peaceful moves.
            4. Call the knight's 'get_valid_peaceful_moves' method to get the actual peaceful moves.
            5. Assert that the actual peaceful moves match the expected set.
        """
        with patch.object(chess_engine.game_state, 'is_valid_piece', return_value=False):
            board = self.test_game_state
            knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
            board.board[3][4] = knight
            expected_moves = {(5, 3), (5, 5), (4, 6), (4, 2), (2, 2), (2, 6), (1, 3), (1, 5)}
            valid_moves = set(knight.get_valid_peaceful_moves(board))
            self.assertEqual(expected_moves, valid_moves)

    def test_knight_valid_piece_takes_2(self):
        """
         Test the knight piece's valid take moves when an opponent's pawn is in range.

         This test sets up a knight on the board and places an opponent's pawn in a position
         that the knight can take. It verifies that the knight's valid take includes the pawn's position.

         Steps:
         1. Place a knight piece on the board at position (3, 4).
         2. Place an opponent's pawn on the board at position (5, 3).
         3. Define the expected list of valid takes, which includes the pawn's position.
         4. Call the knight's 'get_valid_piece_takes' method to get the actual valid takes.
         5. Assert that the actual valid takes match the expected takes.
         """
        board = self.test_game_state
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        pawn = chess_engine.Pawn('p', 5, 3, Player.PLAYER_2)
        board.board[3][4] = knight
        board.board[5][3] = pawn
        expected_takes = [(5, 3)]
        valid_takes = knight.get_valid_piece_takes(board)
        self.assertEqual(expected_takes, valid_takes)

    def test_knight_valid_peaceful_moves_2(self):
        """
            Test the knight piece's valid peaceful moves when an opponent's pawn is in range.

            This test sets up a knight on the board and places an opponent's pawn in a position
            that the knight can take. It verifies that the knight's valid peaceful moves do not
            include the position of the opponent's pawn, as peaceful moves should not involve taking.

            Steps:
            1. Place a knight piece on the board at position (3, 4).
            2. Place an opponent's pawn on the board at position (5, 3).
            3. Define the expected set of peaceful moves (excluding the pawn's position).
            4. Call the knight's 'get_valid_peaceful_moves' method to get the actual peaceful moves.
            5. Assert that the actual peaceful moves match the expected set.
        """
        board = self.test_game_state
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        pawn = chess_engine.Pawn('p', 5, 3, Player.PLAYER_2)
        board.board[3][4] = knight
        board.board[5][3] = pawn
        expected_takes = {(5, 5), (4, 6), (4, 2), (2, 2), (2, 6), (1, 3), (1, 5)}
        valid_takes = set(knight.get_valid_peaceful_moves(board))
        self.assertEqual(expected_takes, valid_takes)

    def set_full_takes(self):
        """
        Set up the chess board with pawns at specific positions for testing the knight's valid take moves.

        This method places eight opponent pawns on the board in positions where they can be potentially
        taken by a knight. It returns the board with the pawns placed.

        Steps:
        1. Initialize the game state board.
        2. Place opponent pawns at the following positions:
        3. Return the board with the pawns set up.

        Returns:
        board (GameState): The game state with pawns placed in specified positions.
        """
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
        """
           Test the knight piece's valid take moves when surrounded by opponent pawns.

           This test sets up the board using the `set_full_takes` method, which places eight opponent pawns
           in positions where they can be taken by a knight. It verifies that the knight's valid take moves
           include all the positions of the opponent pawns.

           Steps:
           1. Use the `set_full_takes` method to set up the board with opponent pawns.
           2. Place a knight piece on the board at position (3, 4).
           3. Define the expected set of valid takes, which includes the positions of all the opponent pawns.
           4. Call the knight's 'get_valid_piece_takes' method to get the actual valid takes.
           5. Assert that the actual valid takes match the expected set.
       """
        board = self.set_full_takes()
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        board.board[3][4] = knight
        expected_takes = {(5, 3), (5, 5), (4, 2), (2, 2), (1, 3), (1, 5), (2, 6), (4, 6)}
        valid_takes = set(knight.get_valid_piece_takes(board))
        self.assertEqual(expected_takes, valid_takes)

    def test_knight_valid_peaceful_moves_3(self):
        """
           Test the knight piece's valid peaceful moves when surrounded by opponent pawns.

           This test sets up the board using the `set_full_takes` method, which places eight opponent pawns
           in positions where they can be taken by a knight. It verifies that the knight has no valid peaceful
           moves (i.e., moves that do not involve taking another piece) when surrounded by these pawns.

           Steps:
           1. Use the `set_full_takes` method to set up the board with opponent pawns.
           2. Place a knight piece on the board at position (3, 4).
           3. Define the expected list of valid peaceful moves (which should be empty).
           4. Call the knight's 'get_valid_peaceful_moves' method to get the actual peaceful moves.
           5. Assert that the actual peaceful moves match the expected list.
       """
        board = self.set_full_takes()
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        board.board[3][4] = knight
        expected_takes = []
        valid_takes = knight.get_valid_peaceful_moves(board)
        self.assertEqual(expected_takes, valid_takes)


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


class system_tests(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test.

        This method initializes a new game state for each test, providing a fresh chessboard
        for the system tests.
        """
        self.test_game_state = chess_engine.game_state()

    def test_full_game(self):
        """
        Test a sequence of moves and check for game state result.

        This test performs a series of moves on the chessboard and verifies the game's state
        is a checkmate.

        Steps:
        1. Move a piece from (1, 2) to (2, 2). (white pawn)
        2. Move a piece from (6, 3) to (4, 3). (black pawn)
        3. Move a piece from (1, 1) to (3, 1). (white pawn)
        4. Move a piece from (7, 4) to (3, 0). (black queen)
        5. Call the 'checkmate_stalemate_checker' method to evaluate the game state.
        6. Assert that the result of the checker method is 0 (indicating checkmate).
        """
        board = self.test_game_state
        board.move_piece((1, 2), (2, 2), False)
        board.move_piece((6, 3), (4, 3), False)
        board.move_piece((1, 1), (3, 1), False)
        board.move_piece((7, 4), (3, 0), False)
        self.assertEqual(board.checkmate_stalemate_checker(), 0)


if __name__ == '__main__':
    unittest.main()
