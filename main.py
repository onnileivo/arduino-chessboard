import chess

cboard = chess.Board()


def main():
    askModeLoop = True
    while askModeLoop:
        gamemode = input("Are you playing on a board or not? (y/n): ")
        if gamemode == "n":
            askModeLoop = False
            import testing

            testing.main()
        elif gamemode == "y":
            askModeLoop = False
            import board

            board.main()
        else:
            print("not a valid mode try again \n")


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

