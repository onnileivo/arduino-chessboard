import pyfirmata
import time
from stockfish import Stockfish
import chess
print("Starting the chessboard arduino project so cool")
print("using 2048 hash (memory) and 18 depth")
stockfish = Stockfish(depth=18, parameters={"Hash": 2048})

# global BYTE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cboard = chess.Board()
# board = pyfirmata.Arduino('/dev/ttyACM0')

# ex_byte = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#Setup pins for communication with a 74HC595 shift register
latchPin = 8
clockPin = 12
dataPin = 11


def main():
    # Startup
    print(stockfish.get_board_visual())
    wantedelo = int(input("Stockfish elo (difficulty) : "))
    stockfish.set_elo_rating(wantedelo)
    wantedskillrating = int(input("Stockfish skill level (difficulty) : "))
    stockfish.set_skill_level(wantedskillrating)
    print("You are playing as whitei")
    print("--------------------------------------------------------")
    print("Moves should be inputted in the format 'a1b2' \n")

    # Game loop
    loop = True
    while loop == True:
        print(stockfish.get_board_visual())
        
        loop2 = True
        while loop2 == True:
            nextmove = askformove()
            if stockfish.is_move_correct(nextmove) and nextmove != "":
                loop2 = False
            else:
                print("Move incorrect try again.")
        
        stockfish.make_moves_from_current_position({nextmove})
        print(stockfish.get_board_visual())
        print("Calculating best move")
        bestmove = stockfish.get_best_move()
        stockfish.make_moves_from_current_position({bestmove})
        print("done")
        bestmove = ""
        nextmove = ""


        if canGameContinue() == False:
            loop = False

# Shift register help functions
def updateShiftRegister(byte): 
   board.digital[latchPin].write(0)
   for i in byte: 
       board.digital[dataPin].write(i)
       board.digital[clockPin].write(1)
       board.digital[clockPin].write(0)
   board.digital[latchPin].write(1)

def turnOn2LedsByte(numA,num1):
    numA = numA - 1 
    num1 = num1 - 1 
    byte = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    byte[numA] = 1
    byte[num1] = 1
    updateShiftRegister(byte)

# Turns on a specified led on the first shift register which controls the leds vamos
def ledOnShiftregister(led_number):
    led_number = led_number - 1
    byte = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    byte[led_number] = 1
    updateShiftRegister(byte)

# GAME LOGIC
def askformove():
    nextinputmove = input("your move: ")
    return nextinputmove

def canGameContinue():
    fenpos = stockfish.get_fen_position()
    cangamecontinue=stockfish.is_fen_valid(fenpos)
    cboard.set_fen(fenpos)
    
    if cboard.is_checkmate():
        print("Checkmate!!!!! well played.")
        return False
    elif cboard.is_stalemate():
        print("Stalemate!!!! its a tie.")
        return False
    elif cangamecontinue == False:
        print("some other wierd stuff happened, the game is over but its not checkmate nor stalemate.")
        return False
    else:
        return True

if __name__ == "__main__":
    main() 
