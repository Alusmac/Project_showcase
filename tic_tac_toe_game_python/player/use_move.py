from tic_tac_toe_game_python.board.update import update


def use_move(board, index, symbol):
    """ Apply the move to the board
    """
    return update(board, index, symbol)
