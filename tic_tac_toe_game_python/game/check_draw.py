def check_draw(board):
    """Checks if anyone has not win
    """
    return all(not cell.isdigit() for cell in board)
