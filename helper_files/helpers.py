import pygame

from helper_files.constants import FIRST_PIECE, NEXT_PIECE_OFFSET, FIRST_PIECE, NEXT_PIECE_OFFSET
from helper_files.constants import BOARD_START, BOARD_DIMENSIONS, ANTIALIAS_SETTING
from helper_files.constants import ADD_TUPLE, SUB_TUPLE, MULT_TUPLE, ADD_DIGIT, SUB_DIGIT, MULT_DIGIT
from helper_files.constants import TEXT_BOX_OFFSET, TEXT_BOX_CORNER, OPTION_BORDER, TEXT_BOX_GREEN

#HELPER FUNCTIONS
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
    
#Create a text box
def create_box(screen, font, text, loc, box):
    tl = tuple_op(loc, TEXT_BOX_OFFSET, SUB_TUPLE)
    br = tuple_op(tl, box, ADD_TUPLE)

    pygame.draw.rect(screen, TEXT_BOX_GREEN, (tl, box), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (tl, box), border_radius = TEXT_BOX_CORNER, width = OPTION_BORDER)
    write_text(text, screen, font, "black", loc)

    return tl, br

#Checks if a player can place a move now
def can_play(current_color, player_name, player_color):
    if current_color == player_color and player_name != "player":
        return False
    return True

#Create a new board
def create_new_board():
    board = [[0 for i in range(8)] for j in range(8)]
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2

    return board