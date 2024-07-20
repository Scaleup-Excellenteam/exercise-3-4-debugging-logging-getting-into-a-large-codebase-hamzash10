import unittest
from unittest.mock import patch

import chess_engine
from enums import Player


class unit_tests(unittest.TestCase):

    def setUp(self):
        """
        Initialize an empty 8x8 chess board for testing purposes.
        This method is called before every test case.
        """
        self.test_game_state = chess_engine.game_state()
        self.test_game_state.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]

    def _set_full_takes(self):
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
        board = self._set_full_takes()
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
        board = self._set_full_takes()
        knight = chess_engine.Knight('n', 3, 4, Player.PLAYER_1)
        board.board[3][4] = knight
        expected_takes = []
        valid_takes = knight.get_valid_peaceful_moves(board)
        self.assertEqual(expected_takes, valid_takes)

if __name__ == '__main__':
    unittest.main()
