import chess
import chess.pgn
import serial
from IPython.display import SVG, display
#import voice
import os, time, keyboard

import speech_recognition as sr
import string

def record():
    while True:
        print("Press space to speak a move.")
        keyboard.wait('space')
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Speak something!")
            audio = r.listen(source,timeout = 5, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio)
            text.lower()
            if(text[2] != " "):
                print("processing")
                text1 = text[0:2] + " "
                text2 = text[2:4]
                text = text1+text2   
            if((text[0].isalpha() and text[3].isalpha()) and (text[1].isdigit() and text[4].isdigit())):
                print("You said: ", text)
                return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            print("Sorry, an error occurred while trying to recognize your speech. Error: ", e)

""" Upload the board object to the website (SVG) and microcontroller () """
def upload_board(board):

    svg = chess.svg.board(board=board)
    #save the SVG image to a file
    with open("chessboard.svg", "w") as f:
        f.write(svg)
    print(type(board))

    # create a 2-D array representing the chess board
    board_array = [[' ' for _ in range(8)] for _ in range(8)]

    # assign each piece on the board to the corresponding element in the array
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            file_number = chess.square_file(square)
            rank_number = chess.square_rank(square)
            piece_name = piece.symbol()
            board_array[rank_number][file_number] = piece_name

    # print the resulting 2-D array
    for row in board_array:
        print(row)
    
    # convert the 2D array to a string
    string = ""
    for row in board_array:
        for value in row:
            string += str(value) + ","
    string = string[:-1] + "\n"

    # send the string to the Arduino via serial communication
    ser = serial.Serial('COM3', 9600) # replace 'COM3' with the serial port of your Arduino
    ser.write(string.encode())
    ser.close()

""" Display the board """
def display_board(board):
    #display(SVG(chess.svg.board(board=board)))
    boardsvg = (chess.svg.board(board))
    with open('temp.svg', 'w') as outputfile:
        outputfile.write(boardsvg)
    time.sleep(0.1)
    os.startfile('temp.svg')


""" Get the move from the player """
def get_move(board, input_type, versus_type):
    legal_moves = board.legal_moves
    if(input_type == "Voice"):
        #voice_condition = 0 # track whether it failed or was successful (or break out of loop)
        while(True):
            v_move = record()
            print("debug: ", v_move, type(v_move))
            #v_move = v_move.strip().replace(" ", "").lower()
            if(v_move.__contains__(" ")):
                v_move = v_move.replace(" ", "")
            v_move = v_move.strip()
            v_move = v_move.lower()
            if(chess.Move.from_uci(v_move) in legal_moves):
                print("Allowed move. Your move was: ", v_move)
                v_move = chess.Move.from_uci(v_move)
                return v_move
            else:
                print("Disallowed move. Try again. Your move was: ", v_move)
    


""" Initialize the board from settings and begin the game """
def initialize_game():
    board = chess.Board()
    # you should import settings from the website
    #settings = website.settings()
    input_type = "Voice"
    versus_type = "CPU"
    return board, input_type, versus_type 

""" Code for ending the match """
def finish_game():
    print('You won!')

if __name__ == "__main__":
    while True:
        board, input_type, versus_type = initialize_game()

        while not board.is_game_over():
            move = get_move(board, input_type, versus_type)
            board.push(move)
            display_board(board)
        #upload_board(board)
