import pyfirmata
import time
from stockfish import Stockfish
import chess
print("Starting the chessboard arduino project so cool")
print("using 2048 hash (memory) and 18 depth")
stockfish = Stockfish(depth=18, parameters={"Hash": 2048})



board = pyfirmata.Arduino('/dev/ttyACM0')

# ex_byte = [0, 0, 0, 0, 0, 0, 0, 0]

#Setup pins for communication with a 74HC595 shift register
latchPinA = 8
clockPinA = 12
dataPinA = 11

latchPin1 = 8
clockPin1 = 12
dataPin1 = 11



# SHIFT REGISTER CONTROLLING
def updateShiftRegisterA(byte): 
   board.digital[latchPinA].write(0)
   for i in byte: 
       board.digital[dataPinA].write(i)
       board.digital[clockPinA].write(1)
       board.digital[clockPinA].write(0)
   board.digital[latchPinA].write(1)

def updateShiftRegister1(byte): 
   board.digital[latchPinA].write(0)
   for i in byte: 
       board.digital[dataPinA].write(i)
       board.digital[clockPinA].write(1)
       board.digital[clockPinA].write(0)
   board.digital[latchPinA].write(1)

# Turns on a specified led on the first shift register which controls the horizontal leds on the chessboard
def ledOnShiftregister_A(led_number):
    led_number = led_number - 1
    byte = [0, 0, 0, 0, 0, 0, 0, 0]
    byte[led_number] = 1
    updateShiftRegisterA(byte)
    
def AllLedOffShiftregister_A():
    byte = [0, 0, 0, 0, 0, 0, 0, 0]
    updateShiftRegisterA(byte)
    
def ledOnShiftregister_1(led_number):
    led_number = led_number - 1
    byte = [0, 0, 0, 0, 0, 0, 0, 0]
    byte[led_number] = 1
    updateShiftRegister1(byte)
    
def AllLedOffShiftregister_1():
    byte = [0, 0, 0, 0, 0, 0, 0, 0]
    updateShiftRegister1(byte)
    
    
    
# GAME LOGIC
def askformove():
    nextinputmove = input("your move: ")
    return nextinputmove

def main():
    # Startup
    print(stockfish.get_board_visual())
    wantedelo = int(input("Stockfish elo (difficulty) : "))
    stockfish.set_elo_rating(wantedelo)
    wantedskillrating = int(input("Stockfish skill level (difficulty) : "))
    stockfish.set_skill_level(wantedskillrating)
    print("You are playing white")
    print("--------------------------------------------------------")
    print("Moves should be inputted in the format 'a1b2' ")
    print("\n")
    
    
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
        
        print(stockfish.get_board_visual())
        print("Calculating best move")
        bestmove = stockfish.get_best_move()
        stockfish.make_moves_from_current_position({bestmove})
        print("done")
        bestmove = ""
        nextmove = ""
        
        # TODO: MAKE BETTER WIN AND STALEMATE CONDITION could do something with evaluation
        cangamecontinue=stockfish.is_fen_valid(stockfish.get_fen_position())
        cboard = chess.Board()
        cboard.set_fen(stockfish.get_fen_position)
        if cboard.is_checkmate():
            print("Checkmate!!!!! well played.")
            loop = False
        elif cboard.is_stalemate():
            print("Stalemate!!!! its a tie.")
            loop = False
        if cangamecontinue == False:
            print("some other wierd stuff happened, the game is over but its not checkmate nor stalemate.")
            loop = False

main()
