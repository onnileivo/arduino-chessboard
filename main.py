import chess


print("Starting the chessboard arduino project so cool")
cboard = chess.Board()


def main():
    gamemode = input("Are you playing on board or not? (y/n): ")
    if gamemode == "n":
        # testing
        import testing

        testing.main()
    elif gamemode == "y":
        import board

        board.main()


# GAME LOGIC
def askformove():
    nextinputmove = input("your move: ")
    return nextinputmove


def canGameContinue(fenpos):
    cboard.set_fen(fenpos)
    if cboard.is_checkmate():
        print("Checkmate!!!! well played.")
        return False
    elif cboard.is_stalemate():
        print("Stalemate!!!! its a tie.")
        return False
    else:
        return True


if __name__ == "__main__":
    main()

