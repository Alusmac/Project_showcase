def look_move(name: int, symbol: int) -> int:
    """Get the move from the user using the keyboard
    """
    while True:
        try:
            user_input = int(input(f"{name} ({symbol}), Put number (1-9): ")) - 1
            if 0 <= user_input <= 8:
                return user_input
            print("Put number must be between 1 and 9")
        except ValueError:
            print("Enter the correct number ")
