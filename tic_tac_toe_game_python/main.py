from tic_tac_toe_game_python.game.play import play


def main():
    print("🏁🏁🏁Wellcome to Tic Tac Toe Game!🏁🏁🏁")

    name1 = input("Name of the first Player (X): ")
    name2 = input("Name of the second Player (O): ")

    player1 = (name1, "X")
    player2 = (name2, "O")

    play(player1, player2)


if __name__ == "__main__":
    main()
