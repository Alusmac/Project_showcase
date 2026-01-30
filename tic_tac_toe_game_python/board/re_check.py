def re_check(board: int|list, index: int) -> bool:
    """Checks whether the box is free
    """
    return board[index].isdigit()
