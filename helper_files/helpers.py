import pygame
import os
from datetime import datetime
from helper_files.constants import *

#HELPER FUNCTIONS
#Copys 2D List
def copy_2d_list(list_to_copy):
    new_list = []
    for i in list_to_copy:
        internal_list = []
        for j in i:
            internal_list.append(j)
        new_list.append(internal_list)

    return new_list

#Switches between colors
def switch_colors(color):
    if color == 1:
        return 2
    return 1

#Removes an element within an array. If error, then nothing happens.
def try_remove(array, item):
    try:
        array.remove(item)
    except:
        pass
    return array

#Get location of the a specified piece
def get_piece_location(x, y):
    return (FIRST_PIECE[0] + x * NEXT_PIECE_OFFSET, FIRST_PIECE[1] + y * NEXT_PIECE_OFFSET)

#Checks if pixel coordinates are located within the board
def within_board(x, y):
    return x >= BOARD_START[0] and x <= BOARD_START[0] + BOARD_DIMENSIONS[0] and y >= BOARD_START[1] and y <= BOARD_START[1] + BOARD_DIMENSIONS[1] 

#Checks if board coordinates are located within the board
def within_board_coords(x, y):
    return x <= 7 and x >= 0 and y <= 7 and y >= 0

#Checks if pixel coordinates are located within the box
def within_box(x, y, box_tl, box_br):
    return x >= box_tl[0] and x <= box_br[0] and y >= box_tl[1] and y <= box_br[1]

#Gets all the moves valid and the resulting changes.
def all_moves(board, color):
    moves = []
    removed = []
    other_color = switch_colors(color)

    for x in range(8):
        for y in range(8):
            move_removed = []
            validSpace = False
            opp_color_directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != j or i != 0]
            #If space is blank
            if board[x][y] == 0:
                #Remove edge cases for x + y from locations where opposite color could be
                if x == 0:
                    opp_color_directions = try_remove(opp_color_directions, (-1, 0))
                    opp_color_directions = try_remove(opp_color_directions, (-1, 1))
                    opp_color_directions = try_remove(opp_color_directions, (-1, -1))
                elif x == 7:
                    opp_color_directions = try_remove(opp_color_directions, (1, 0))
                    opp_color_directions = try_remove(opp_color_directions, (1, 1))
                    opp_color_directions = try_remove(opp_color_directions, (1, -1))

                if y == 0:
                    opp_color_directions = try_remove(opp_color_directions, (-1, -1))
                    opp_color_directions = try_remove(opp_color_directions, (1, -1))
                    opp_color_directions = try_remove(opp_color_directions, (0, -1))
                elif y == 7:
                    opp_color_directions = try_remove(opp_color_directions, (-1, 1))
                    opp_color_directions = try_remove(opp_color_directions, (1, 1))
                    opp_color_directions = try_remove(opp_color_directions, (0, 1))
                
                #Remove all directions where opposite color isn't there
                for i, j in opp_color_directions:
                    x_new = x
                    y_new = y
                    if board[x + i][y + j] == other_color:
                        x_new += i
                        y_new += j
                        tempRemoved = []
                        #Iterate till you find the other end or a blank space
                        while within_board_coords(x_new, y_new):
                            if board[x_new][y_new] == color:
                                validSpace = True
                                move_removed.extend(tempRemoved)    
                                break                    
                            elif board[x_new][y_new] == 0:
                                break
                            else:
                                tempRemoved.append((x_new, y_new))

                            x_new += i
                            y_new += j

                if validSpace:
                    moves.append((x,y))
                    removed.append(move_removed) 
    
    movesKeys = [str(i) + str(j) for i, j in moves]
    moveDict = dict(map(lambda i,j : (i,j) , movesKeys, removed))
    return moves, moveDict

#Counts pieces for black and white
def count_pieces(board):
    whiteCount = 0
    blackCount = 0

    for x in range(8):
        for y in range(8):
            if board[x][y] == 1:
                whiteCount += 1
            elif board[x][y] == 2:
                blackCount += 1
    
    return whiteCount, blackCount

#Writes text
def write_text(text, screen, font, color, location):
    textSurface = font.render(text, ANTIALIAS_SETTING, color)
    screen.blit(textSurface, location)

#Tuple operations
def tuple_op(tuple_1, num_2, operation):
    if operation == ADD_TUPLE:
        return (tuple_1[0] + num_2[0], tuple_1[1] + num_2[1])
    elif operation == SUB_TUPLE:
        return (tuple_1[0] - num_2[0], tuple_1[1] - num_2[1])
    elif operation == MULT_TUPLE:
        return (tuple_1[0] * num_2[0], tuple_1[1] * num_2[1])
    elif operation == ADD_DIGIT:
        return (tuple_1[0] + num_2, tuple_1[1] + num_2)
    elif operation == SUB_DIGIT:
        return (tuple_1[0] - num_2, tuple_1[1] - num_2)
    elif operation == MULT_DIGIT:
        return (tuple_1[0] * num_2, tuple_1[1] * num_2)

#Create a colored text box
def create_box_color(screen, font, text, loc, box, color):
    tl = tuple_op(loc, TEXT_BOX_OFFSET, SUB_TUPLE)
    br = tuple_op(tl, box, ADD_TUPLE)

    pygame.draw.rect(screen, color, (tl, box), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (tl, box), border_radius = TEXT_BOX_CORNER, width = OPTION_BORDER)
    write_text(text, screen, font, "black", loc)

    return tl, br

#Checks if a player can place a move now
def can_play(current_color, player_name, player_color):
    if current_color == player_color and player_name != "player":
        return False
    return True

#Selects a specific box
def select_box(color_list, number, select_type):
    new_color_list = []

    if select_type == "diff":
        new_color_list.append(number)
        for i in color_list:
            if i >= 5:
                new_color_list.append(i)
    elif select_type == "color":
        new_color_list.append(number)
        for i in color_list:
            if i < 5:
                new_color_list.append(i)
    else:
        print("Select Error.")
        new_color_list = color_list

    return new_color_list

#Get Selections
def get_selections(color_list):
    info_dict = {0 : "player", 1 : "easy", 2 : "medium", 3 : "hard", 4: "expert", 5: 1, 6: 2}
    player_name = "player"
    player_color = 1

    for i in color_list:
        if i < 5:
            player_name = info_dict[i]
        else:
            player_color = info_dict[i]

    return (player_name, player_color)

#Create a new board
def create_new_board():
    board = [[0 for i in range(8)] for j in range(8)]
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2

    return board

#Returns scoring of the current position given a certain heuristic
def get_score_ml(board, heuristic):
    white_score = 0
    black_score = 0

    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                white_score += heuristic[i][j]
            elif board[i][j] == 2:
                black_score += heuristic[i][j]

    return (white_score, black_score)

#Get score of board for a color 
def evaluate_board(board, heuristic, ai_color):
    scoring = get_score_ml(board, heuristic)

    if ai_color == 1:
        score = scoring[0] - scoring[1]
    else:
        score = scoring[1] - scoring[0]

    return score

#Making a move for a prediciton algorithm
def make_move_pred(old_board, move, moveDict, color):
    board = copy_2d_list(old_board)
    x_coord, y_coord = move
    strCoords = str(x_coord) + str(y_coord)
    board[x_coord][y_coord] = color
    for i, j in moveDict[strCoords]:
        board[i][j] = color
    
    return board

#Algorithm
def min_max(board, heuristic, ai_color, curr_color, depth, is_ai, numSkips, outsideCall):
    gameOver = numSkips >= 2
    moves, moveDict = all_moves(board, curr_color)
    move_to_make = None

    if depth == 0 or gameOver:
        value = evaluate_board(board, heuristic, ai_color) 
    elif len(moves) == 0:
        new_color = switch_colors(curr_color)
        value = min_max(board, heuristic, ai_color, new_color, depth, not is_ai, numSkips + 1, False)
    elif is_ai:
        value = -999999
        
        for move in moves:
            temp_board = make_move_pred(board, move, moveDict, curr_color)
            new_color = switch_colors(curr_color)
            prev_value = value
            value = max(value, min_max(temp_board, heuristic, ai_color, new_color, depth - 1, False, 0, False))
            if prev_value != value and outsideCall:
                move_to_make = move
    else:
        value = 999999
        for move in moves:
            temp_board = make_move_pred(board, move, moveDict, curr_color)
            new_color = switch_colors(curr_color)
            value = min(value, min_max(temp_board, heuristic, ai_color, new_color, depth - 1, True, 0, False))
    
    if not outsideCall:
        return value
    else:
        return move_to_make

#Get datetime from file name of log_files
def get_datetime_from_log_file(log_file):
    underscore_count = 0
    datetime_string = ''
    for i in log_file:
        if i == '_':
            underscore_count += 1
        elif underscore_count >= 4:
            datetime_string += i
    return datetime_string

#Remove old log_files
def remove_old_log_files():
    files = [i for i in os.listdir('logs') if i[:11] == "othello_log"]
    if len(files) > 9:
        dateDict = {}
        dates = []
        for file in files:
            dateStr = get_datetime_from_log_file(file)[:-4]
            date = datetime.strptime(dateStr, "%Y%m%d-%H%M%S")
            dateDict[dateStr] = file
            dates.append(date)
        for i in range(10):
            newest = max(dates)
            newStr = newest.strftime("%Y%m%d-%H%M%S")
            poppedFile = dateDict[newStr]
            dates.remove(newest)
            files.remove(poppedFile)
        for file in files:
            os.remove(f"logs/{file}") 

#Output Board
def output_board(board, num_moves, player, file:None):
    if player[0] == "player":
            name = "pvp"
    else:
            name = player[0]

    output_string = f"Board #{num_moves} vs {name}:\n"
    for i in board:
        new_line = []
        for j in i:
            if j == 0:
                new_line.append(' ')
            elif j == 1:
                new_line.append('W')
            else:
                new_line.append('B')
        output_string += str(new_line) + "\n"

    if LOG_LOCATION == LOG_TO_PRINT:
        print(output_string)
    elif LOG_LOCATION == LOG_TO_FILE:
        remove_old_log_files()
        now = datetime.now()
        datetimestring = now.strftime("%Y%m%d-%H%M%S")
        
        if player[1] == 1:
            color = "b"
        else:
            color = "w"
 
        if file == None:
            file_name = f"othello_log_{name}_{color}_{datetimestring}.txt"
            file_location = f"logs/{file_name}"
            directory_exists = os.path.isdir("logs")
            if not directory_exists:
                os.mkdir("logs")
            try:
                with open(file_location, "x") as f:
                    f.write(output_string)
            except Exception as e:
                print(f"File {file_name} Exists!")        
        else:
            file_name = file
            file_location = f"logs/{file_name}"
            with open(file_location, "a") as f:
                f.write(output_string)

        return file_name
    elif LOG_LOCATION == NO_LOG:
        pass
    else:
        print("Invalid Log Location.")

    return None