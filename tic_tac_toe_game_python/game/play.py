from tic_tac_toe_game_python.board.build import build
from tic_tac_toe_game_python.board.display import display
from tic_tac_toe_game_python.player.look_move import look_move
from tic_tac_toe_game_python.player.use_move import use_move
from tic_tac_toe_game_python.player.check_move import check_move
from tic_tac_toe_game_python.game.check_win import check_win
from tic_tac_toe_game_python.game.check_draw import check_draw
from tic_tac_toe_game_python.game.change_player import change_player


def play(player1, player2):
    """ playing board with moving and changing players
    """
    board = build()
    players = [player1, player2]
    current = 0

    while True:
        display(board)

        name, symbol = players[current]
        index = look_move(name, symbol)

        if not check_move(board, index):
            print("This area is busy! Please select another one.")
            continue

        use_move(board, index, symbol)

        if check_win(board, symbol):
            display(board)
            print(f"🏆 Winner: {name} ({symbol})!")
            break

        if check_draw(board):
            display(board)
            print("Ended in a draw!")
            break

        current = change_player(current)
