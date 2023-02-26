import chess
import chess.pgn
import chess.engine
import serial
from IPython.display import SVG, display
import os, time, keyboard

import speech_recognition as sr
import string

import speech_recognition as sr
import string
import keyboard

""" Record audio for voice commands """
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

    print(string)

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

""" Get stockfish's move (black only) """
def get_stockfish_move(board):
    # Initialize the Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci("C:/hackathon_dekat/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2")

    # Set the position to the current board state
    info = engine.analyse(board, chess.engine.Limit(time=2.0))

    # Get the best move suggested by Stockfish
    best_move = info.get("pv")[0]

    # Stop the engine
    engine.quit()

    return best_move


""" Get the move from the player """
def get_move(board, input_type, versus_type):
    if board.turn == chess.BLACK:
        # It is black's turn, so get a move suggestion from Stockfish
        move = get_stockfish_move(board)
        return move

    # Get all legal moves on the board
    legal_moves = board.legal_moves

    if(input_type == "Voice"):
        #voice_condition = 0 # track whether it failed or was successful (or break out of loop)
        while(True):
            v_move = record()
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

# Define a function to update the elapsed time for a player
def update_time(player, elapsed_time, white_time, black_time):
    if player == chess.WHITE:
        white_time -= elapsed_time
    else:
        black_time -= elapsed_time
    return white_time, black_time


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
    # Check the result of the game
    result = board.result()

    # Return a string based on the result
    if(result == "1-0"):
        return "White wins!"
    if(result == "0-1"):
        return "Black wins!"
    if(result == "1-2/1-2"):
        return "Drawn match!"
    else:
        return "Error: Unknown match result."

if __name__ == "__main__":
    while(True):
        #await
        print('hi')
        break

    board, input_type, versus_type = initialize_game()
    # Set the initial time for both players
    white_time = 15 * 60  # 5 minutes
    black_time = 15 * 60  # 5 minutes
    # Set the time increment for both players
    time_increment = 10  # 5 seconds

    

    while not board.is_game_over():
        # Determine the current player
        current_player = board.turn

        # Get the current time
        start_time = time.time()

        # Get the move from the player
        move = get_move(board, input_type, versus_type)

        # Determine the elapsed time for the move
        elapsed_time = int(time.time() - start_time)

        # Update the elapsed time for the current player
        white_time, black_time = update_time(current_player, elapsed_time, white_time, black_time)

        # Add the time increment to the current player's time
        if current_player == chess.WHITE:
            white_time += time_increment
        else:
            black_time += time_increment

        # Push the move to the board
        board.push(move)

        # Print the current time for both players
        print(f"White: {white_time // 60}:{white_time % 60:02d}")
        print(f"Black: {black_time // 60}:{black_time % 60:02d}")

        display_board(board)
        #upload_board(board)
        final_message = finish_game()
