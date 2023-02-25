import chess
import chess.pgn
import serial
#import voice

if __name__ == "__main__":
    board = chess.Board()
    print(board)
    svg = chess.svg.board(board=board)

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
    ser = serial.Serial('COM3', 9600) # replace 'COM3' with the serial port of your Arduino
    ser.write(string.encode())
    ser.close()

    # # print the resulting 2-D array
    # for row in board_array:
    #     print(row)
    print(string)






    # save the SVG image to a file
    # with open("chessboard.svg", "w") as f:
    #     f.write(svg)
    # print(type(board))
