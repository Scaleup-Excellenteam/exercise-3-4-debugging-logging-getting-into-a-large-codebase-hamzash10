import chess_engine


def main():
    white_moves = [((1, 2), (2, 2)),  # pawn B3 -> C3
                   ((1, 1), (3, 1))]  # queen B2 -> D2

    black_moves = [((6, 3), (4, 3)),  # pawn moves from G4 to E4
                   ((7, 4), (3, 0))]  # queen H5 -> D1 checkmate

    game_state = chess_engine.game_state()  # Initialize the game state

    for white_move, black_move in zip(white_moves, black_moves):
        game_state.move_piece(white_move[0], white_move[1], False)
        game_state.move_piece(black_move[0], black_move[1], False)

    game_state.checkmate_stalemate_checker()  # Check the game state for checkmate or stalemate


if __name__ == '__main__':
    main()
