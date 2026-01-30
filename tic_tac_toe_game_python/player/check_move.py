from tic_tac_toe_game_python.board.re_check import re_check


def check_move(board, index):
    """Check if a move is legal or not
    """
    return re_check(board, index)
