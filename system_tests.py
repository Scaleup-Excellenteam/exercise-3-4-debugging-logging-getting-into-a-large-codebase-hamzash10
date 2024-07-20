import unittest
import chess_engine


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
