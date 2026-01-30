from .re_check import re_check


def update(board: int|list, index: int, symbol: str | int) -> bool:
    """Put an X or O on the board
    """
    if re_check(board, index):
        board[index] = symbol
        return True
    return False
