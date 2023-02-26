import chess
import chess.pgn
import chess.engine
import serial
from IPython.display import SVG, display
import os, time, keyboard

import speech_recognition as sr
import string
import keyboard

ser = serial.Serial('COM7', 9600) # replace 'COM3' with the appropriate serial port and baud rate

""" Sends LED data to the Arduino in the form of rows and columns """
def set_led(row, col, state):
    command = f's {row} {col} {int(state)}\n'
    ser.write(command.encode())

"""" Cleans up strings and converts string into 2D array of 8x8 """
def display(board):
    time.sleep(2)
    board = board.replace(",", "")
    edit_board = []
    for i in range(8):
        edit_board.append(board[i*8:(i+1)*8])
    # turn on the first row
    for col in range(8):
        for row in range(8):
            if(edit_board[col][row]!= " "):
                set_led(row, col, True)
            else:
                set_led(row, col, False)

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
            if(len(text)> 4 and (text[0].isalpha() and text[3].isalpha()) and (text[1].isdigit() and text[4].isdigit())):
                print("You said: ", text)
                return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            print("Sorry, an error occurred while trying to recognize your speech. Error: ", e)

""" Upload the board object to the website (SVG) and microcontroller (8x8 array) """
def upload_board(board):

    svg = chess.svg.board(board=board)
    #save the SVG image to a file
    with open("web/src/assets/chessboard.svg", "w") as f:
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
    
    # convert the 2D array to a string
    string = ""
    for row in board_array:
        for value in row:
            string += str(value) + ","
    string = string[:-1] + "\n"

    # send the string to the Arduino via serial communication
    display(string)

""" Display the board """
def display_board(board):
    #display(SVG(chess.svg.board(board=board)))
    boardsvg = (chess.svg.board(board))
    #with open('web/src/assets/temp.svg', 'w') as outputfile:
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

""" The engine cannot natively handle promotions with 4-char UCI commands. This handles that. """
def handle_promotion(board, move):
    if(move[1] == '2' and move[3] == '1'):
        if(chess.Move.from_uci(str(move + 'q')) in board.legal_moves):
            return (move + 'q')
    elif(move[1] == '7' and move[3] == '8'):
        if(chess.Move.from_uci(str(move + 'q')) in board.legal_moves):
            return (move + 'q')
    return move

""" Get the move from the player """
def get_move(board, input_type, versus_type):
    if(versus_type == "CPU"):
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
            v_move = handle_promotion(board, v_move)
            if(chess.Move.from_uci(v_move) in legal_moves):
                print("Allowed move. Your move was: ", v_move)
                v_move = chess.Move.from_uci(v_move)
                return v_move
            else:
                print("Disallowed move. Try again. Your move was: ", v_move)  
    else:
        while(True):
            # Get user input for the next move in UCI format
            k_move = input("Enter your move (in UCI format): ")

            k_move = handle_promotion(board, k_move)
            if(chess.Move.from_uci(k_move) in legal_moves):
                print("Allowed move. Your move was: ", k_move)

                # Parse the user input to obtain the corresponding move object
                k_move = chess.Move.from_uci(k_move)

                return k_move
            else:
                print("Disallowed move. Try again. Your move was: ", k_move)



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
    input_type = "Voice"
    versus_type = "CPU"
    return board, input_type, versus_type 

""" Code for ending the match """
def finish_game(board):
    # Check the result of the game
    result = board.result()

    display_board(board)
    upload_board(board)

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

    # Initialize the game
    board, input_type, versus_type = initialize_game()

    # Set the initial time for both players
    white_time = 15 * 60  # 5 minutes
    black_time = 15 * 60  # 5 minutes

    # Set the time increment for both players
    time_increment = 10  # 5 seconds

    # While the game is ongoing
    while not board.is_game_over():
        # Display the board
        display_board(board)

        # Upload the board to embedded/web connections
        upload_board(board)

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

    # Get the final standing of the game
    final_message = finish_game(board)
    print("\n" + final_message)
