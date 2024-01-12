from stockfish import Stockfish
from main import askformove, canGameContinue
from pyfirmata import Arduino
import time

board = Arduino("dev/ttyAMC0")
print("Starting the chessboard arduino project so cool")
print("using 2048 hash (memory) and 18 depth")
stockfish = Stockfish(depth=18, parameters={"Hash": 2048})

# setup pins for communication with a 74HC595 shift register
latchPin = 8
clockPin = 12
dataPin = 11

numberdict = {
    "a": "1",
    "b": "2",
    "c": "3",
    "d": "4",
    "e": "5",
    "f": "6",
    "g": "7",
    "h": "8",
}


def main():
    # Startup
    print(stockfish.get_board_visual())
    wantedelo = int(input("Stockfish elo (difficulty) : "))
    stockfish.set_elo_rating(wantedelo)
    print("--------------------------------------------------------")
    print("Moves should be inputted in the format 'a1b2' \n")

    # Game loop
    loop = True
    while loop is True:
        print(stockfish.get_board_visual())
        bestmove_list = []
        nextmove_list = []
        loop2 = True
        while loop2 is True:
            nextmove = askformove()
            if stockfish.is_move_correct(nextmove) and nextmove != "":
                nextmove_list.append(nextmove)
                loop2 = False
            else:
                print("Move incorrect try again.")

        stockfish.make_moves_from_current_position(nextmove_list)
        print(stockfish.get_board_visual())
        print("Calculating best move")
        bestmove_list.append(stockfish.get_best_move())
        stockfish.make_moves_from_current_position(bestmove_list)
        bestmove = bestmove_list[0]
        showMoveLeds(bestmove)

        if canGameContinue(stockfish.get_fen_position()) is False:
            loop = False


# Shift register help functions
def updateShiftRegister(byte):
    board.digital[latchPin].write(0)
    for i in byte:
        board.digital[dataPin].write(i)
        board.digital[clockPin].write(1)
        board.digital[clockPin].write(0)
    board.digital[latchPin].write(1)


def turnOn2LedsByte(numA, num1):
    numA = numA - 1
    num1 = num1 - 1
    byte = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    byte[numA] = 1
    byte[num1] = 1
    updateShiftRegister(byte)


def showMoveLeds(move):
    emptybyte = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    movelist = list(move)
    movelist[0] = numberdict[movelist[0]]
    movelist[2] = numberdict[movelist[2]]
    m1p1 = int(list[0])
    m1p2 = int(list[1]) + 8
    m2p1 = int(list[2])
    m2p2 = int(list[3]) + 8
    turnOn2LedsByte(m1p1, m1p2)
    time.sleep(1.5)
    updateShiftRegister(emptybyte)
    time.sleep(0.5)
    turnOn2LedsByte(m1p1, m1p2)
    time.sleep(1)
    turnOn2LedsByte(m2p1, m2p2)
    time.sleep(1.5)
    updateShiftRegister(emptybyte)
    time.sleep(0.5)
    turnOn2LedsByte(m2p1, m2p2)
    time.sleep(1)
