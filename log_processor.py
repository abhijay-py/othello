import os
import json
import math
from helper_files.helpers import all_moves, count_pieces, make_move_pred, copy_2d_list

algorithm_list = ["pvp", "easy", "medium", "hard", "expert"]

#Output a board
def output_board(board):
    for i in board:
        print(i)
def boards_are_same(board_one, board_two):
    for i in range(8):
        for j in range(8):
            if board_one[i][j] != board_two[i][j]:
                return False
    
    return True

#Get all log files that exist
def get_log_files(file_directory):
    files = [i for i in os.listdir(file_directory) if i[:11] == "othello_log"]
    return files

#Get the lines from a specified log file
def read_log(file, path_to_file):
    with open(path_to_file+"/"+file, "r") as f:
        text = f.read()
    lines = text.split("\n")

    return lines

#Verify whether the log_file was created correctly
def verify_log_creation(file, lines):
    board_line = True
    counter = 0
    line_counter = 0
    algorithm_text = file[12:]
    algorithm = ""

    for i in algorithm_text:
        if i != '_':
            algorithm += i
        else:
            break
    
    if algorithm not in algorithm_list:
        return counter, False, "File Name Error"

    for line in lines:
        if counter == 0:
            offset = 1
        else:
            offset = int(math.log(counter, 10)) + 1

        if line == '' and board_line:
            return counter - 1, True, algorithm

        if board_line:
            if algorithm != line[11+offset:-1]:
                return counter, False, "Algorithm Name Error"
            if counter != int(line[7:7+offset]):
                return counter, False, "Board Numbering Error"
            counter += 1
            line_counter = 0
        else:
            line_counter += 1
            if line[0] != '[' or line[-1] != ']':
                return counter, False, "Missing Bracket Error"
            if len(line.split(',')) != 8:
                return counter, False, "Row Error"
            
        board_line = not board_line and line_counter % 8 == 0
    
    return counter, True, algorithm

#Extract the boards from the log file's lines
def get_boards(lines):
    boards = []
    board_line = True
    line_counter = 0
    new_board = []
    
    for line in lines:
        if board_line:
            if line_counter != 0:
                boards.append(new_board)
            new_board = []
            if line == '':
                break
            
        else:
            new_line = []

            for i in line.split(","):
                if 'W' in i:
                    new_line.append(1)
                elif 'B' in i:
                    new_line.append(2)
                else:
                    new_line.append(0)
            new_board.append(new_line)
            line_counter += 1
            
        board_line = not board_line and line_counter % 8 == 0

    return boards     

#Get how the game ended.
def get_ending(boards):
    last_board = boards[-1]

    white_all_moves = all_moves(last_board, 1)[0]
    black_all_moves = all_moves(last_board, 2)[0]
    piece_count = count_pieces(last_board)

    if len(white_all_moves) == 0 and len(black_all_moves) == 0:
        return True, piece_count
    
    return False, piece_count

#Validate the move sequence is valid
def validate_move_sequence(boards):
    prev_board = []
    prevIsBlack = True
    for board in boards:
        if len(prev_board) != 0:
            if prevIsBlack:
                color = 1
            else:
                color = 2

            moves, moveDict = all_moves(prev_board, color)
            validMoveExists = False
            for move in moves:
                new_board = make_move_pred(prev_board, move, moveDict, color)
                if boards_are_same(board, new_board):
                    validMoveExists = True
                    break
            
            if not validMoveExists:
                return False

        prevIsBlack = not prevIsBlack
        prev_board = copy_2d_list(board)

    return True

#Process the entirety of a log file (valid, hasEnded, num_boards, alg/error, piece_count)
def process_log_file(file, path_to_file):
    lines = read_log(file, path_to_file)
    num_boards, valid_board, error_text = verify_log_creation(file, lines)

    if not valid_board:
        return False, False, num_boards, error_text, (), []
    
    boards = get_boards(lines)
    validMoves = validate_move_sequence(boards)

    if not validMoves:
        return False, False, num_boards, "Invalid Move Sequence", (), boards

    algorithm = error_text
    hasEnded, piece_count = get_ending(boards)

    return True, hasEnded, num_boards, algorithm, piece_count, boards

def output_log_file_info(file, path_to_file):
    valid, hasEnded, num_turns, info_text, piece_count, boards = process_log_file(file, path_to_file)
    print()

    if not valid:
        print(f"This log file has been initialized incorrectly: {info_text}.")
        print()
        return boards

    if not hasEnded:
        print(f"This game did not end.")
    else:
        print(f"This game did end.")

    blackCount = piece_count[1]
    whiteCount = piece_count[0]
    player_color = file.split("_")[3]


    print(f"After {num_turns} turns, the score was:")
    print(f"White: {whiteCount}")
    print(f"Black: {blackCount}")

    if info_text == "pvp":
        print("This was a two player game.")
    else:
        print(f"The player went up against the {info_text} algorithm.")
        print(f"The {info_text} algorithm played ", end="")
        if player_color == "b":
            print("white.")
        else:
            print("black.")
    
    print()
    return boards


file = get_log_files("logs")[0]
boards = output_log_file_info(file, "logs")
