import pygame
from datetime import datetime, timedelta

#Importing Constants
from constants import ADD_TUPLE, SUB_TUPLE, MULT_TUPLE, ADD_DIGIT, SUB_DIGIT, MULT_DIGIT
from constants import BOARD_GREEN, LIGHT_BOARD_GREEN, BACKGROUND_BLUE, BACKGROUND_GREEN 
from constants import BORDER_RED, TEXT_BOX_ORANGE, SCREEN_DIMENSIONS, LINE_THICKNESS
from constants import BOARD_EDGE_RADIUS, BOARD_DIMENSIONS, BOARD_START, BORDER_THICKNESS
from constants import TURN_LOCATION, BLACK_SCORE_LOCATION, WHITE_SCORE_LOCATION
from constants import PIECE_OFFSET, PIECE_BORDER_THICKNESS, PIECE_RADIUS, FIRST_PIECE
from constants import MENU_TITLE_LOCATION, TEXT_BOX_OFFSET, TITLE_BORDER, TEXT_BOX_CORNER
from constants import MIDMENU_TITLE_BOX, TIME_IDLE_QUIT, FPS, NEXT_PIECE_OFFSET
from constants import MENU_STATE, CREATE_GAME_STATE, GAME_STATE, MENU_MIDGAME_STATE, RESTART_GAME_STATE
from constants import INFO_STATE, CREDITS_STATE, QUIT_STATE, ANTIALIAS_SETTING

#Importing Helpers
from helpers import switch_colors, try_remove, get_piece_location, within_board, within_board_coords
from helpers import within_box, all_moves, count_pieces, write_text, tuple_op

#Importing Text Boxes
from text_boxes import create_menu_box, create_mm_quit, create_rg_box


#STATES
#TODO: ADD BOXES AROUND TEXT
def game_state(board, screen, font, color, pos, turns, mouseClicked):
    #Assign inputs to state variables
    numberOfTurnsSkipped = turns 
    current_color = color

    #Gets all possible moves for the current color. Changes the color if no moves exist. 
    moveList, moveDict = all_moves(board, current_color)

    if len(moveList) == 0:
        current_color = switch_colors(current_color)
        numberOfTurnsSkipped += 1
    else:
        numberOfTurnsSkipped = 0

    #Place a piece down.
    if mouseClicked & within_board(pos[0], pos[1]):
        x, y = pos
        x_coord = int((x - BOARD_START[0]) / NEXT_PIECE_OFFSET)
        y_coord = int((y - BOARD_START[1]) / NEXT_PIECE_OFFSET)

        if board[x_coord][y_coord] == 0 and (x_coord, y_coord) in moveList:
            strCoords = str(x_coord) + str(y_coord)
            board[x_coord][y_coord] = current_color
            for i, j in moveDict[strCoords]:
                board[i][j] = current_color
            current_color = switch_colors(current_color)

    #Fill in the Background
    screen.fill(BACKGROUND_BLUE)

    #Put Turn Text
    if numberOfTurnsSkipped == 0:
        color_word = 'White'
        if current_color == 2:
            color_word = 'Black'
        write_text(color_word + "'s Turn to Move.", screen, font, 'black', TURN_LOCATION)

    elif numberOfTurnsSkipped >= 2:
        whiteCount, blackCount = count_pieces(board)
        if whiteCount > blackCount:
            message = "Game Over. White Won!"
        elif blackCount > whiteCount:
            message = "Game Over. Black Won!"
        else:
            message = "Game Over. It was a Tie."

        write_text(message, screen, font, 'black', TURN_LOCATION)

    #Put Score Text
    whiteCount, blackCount = count_pieces(board)
    write_text(f"White: {whiteCount}", screen, font, 'black', WHITE_SCORE_LOCATION)
    write_text(f"Black: {blackCount}", screen, font, 'black', BLACK_SCORE_LOCATION)

    #Draw the Board
    pygame.draw.rect(screen, BOARD_GREEN, (BOARD_START, BOARD_DIMENSIONS), border_radius = BOARD_EDGE_RADIUS) 

    #Highlight Possible Moves
    for i, j in moveList:
        center = get_piece_location(i, j)
        pygame.draw.rect(screen, LIGHT_BOARD_GREEN, ((center[0] - NEXT_PIECE_OFFSET / 2, center[1] - NEXT_PIECE_OFFSET / 2), (NEXT_PIECE_OFFSET, NEXT_PIECE_OFFSET)))

    #Draw the Lines Around the Board and Through the Board
    pygame.draw.rect(screen, "black", (BOARD_START, tuple_op(BOARD_DIMENSIONS, BORDER_THICKNESS, ADD_DIGIT)), 
                    border_radius = BOARD_EDGE_RADIUS, width = BORDER_THICKNESS)
    line_offset = NEXT_PIECE_OFFSET
    for i in range(7):
        pygame.draw.line(screen, "black", tuple_op(BOARD_START, (line_offset, 0), ADD_TUPLE), 
            tuple_op(BOARD_START, (line_offset, BOARD_DIMENSIONS[1]), ADD_TUPLE), width = LINE_THICKNESS)
        pygame.draw.line(screen, "black", tuple_op(BOARD_START, (0, line_offset), ADD_TUPLE), 
            tuple_op(BOARD_START, (BOARD_DIMENSIONS[0], line_offset), ADD_TUPLE), width = LINE_THICKNESS)
        
        line_offset += NEXT_PIECE_OFFSET

    #Draw Pieces on the Board
    for i in range(8):
        for j in range(8):
            has_piece = False

            if board[i][j] == 1:
                color = "white"
                has_piece = True
            
            elif board[i][j] == 2:
                color = "black"
                has_piece = True

            if has_piece:
                piece_location = get_piece_location(x = i, y = j)        
                pygame.draw.circle(screen, color, piece_location, PIECE_RADIUS)
                pygame.draw.circle(screen, BORDER_RED, piece_location, PIECE_RADIUS, width = PIECE_BORDER_THICKNESS)

    return current_color, numberOfTurnsSkipped

def mid_game_menu_state(screen, regular_font, title_font, pos, mouseClicked):
    #Draw Background
    screen.fill(BACKGROUND_GREEN)

    #Title
    pygame.draw.rect(screen, TEXT_BOX_ORANGE, (tuple_op(MENU_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                MIDMENU_TITLE_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (tuple_op(MENU_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                    MIDMENU_TITLE_BOX), border_radius = TEXT_BOX_CORNER, width = TITLE_BORDER)
    write_text("In-Game Options", screen, title_font, "black", MENU_TITLE_LOCATION)

    #Options (Back to Game, Home Menu, Exit)
    rg_top_left, rg_bot_right = create_rg_box(screen, regular_font)
    menu_tl, menu_br = create_menu_box(screen, regular_font)
    quit_tl, quit_br = create_mm_quit(screen, regular_font)

    #Option Logic
    if mouseClicked:
        if within_box(pos[0], pos[1], rg_top_left, rg_bot_right):
            return GAME_STATE
        elif within_box(pos[0], pos[1], menu_tl, menu_br):
            return MENU_STATE
        elif within_box(pos[0], pos[1], quit_tl, quit_br):
            return QUIT_STATE

    return MENU_MIDGAME_STATE

def menu_state(screen, regular_font, title_font, pos, mouseClicked):
    #Draw Background
    screen.fill(BACKGROUND_GREEN)

    #Spacing Reference Lines (will delete)
    pygame.draw.line(screen, "black", (SCREEN_DIMENSIONS[0]/2, 0), 
        (SCREEN_DIMENSIONS[0]/2, SCREEN_DIMENSIONS[1]), width = LINE_THICKNESS)
    pygame.draw.line(screen, "black", (0, SCREEN_DIMENSIONS[1]/2), 
        (SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]/2), width = LINE_THICKNESS)


    return MENU_STATE


#Create Board and Setup Starting Pieces. 1 Stands for White, 2 Stands for Black.
board = [[0 for i in range(8)] for j in range(8)]
board[3][3] = 1
board[4][4] = 1
board[3][4] = 2
board[4][3] = 2
 
current_color = 2 #Represents Black
numberOfTurnsSkipped = 0 #If gets to two and the timer passes, end game.
end_time = datetime.now() + timedelta(seconds=TIME_IDLE_QUIT) #For when the game ends.
state = GAME_STATE #Works with the States listed in Constants

#Pygame Initialization
pygame.init()
tnrMediumFont = pygame.font.SysFont('Times New Roman', 25)
tnrMenuFont = pygame.font.SysFont('Times New Roman', 35)
tnrLargeFont = pygame.font.SysFont('Times New Roman', 50)
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Othello")
pygame.key.set_repeat()
clock = pygame.time.Clock()
running = True

#Game Loop
while running:
    mouseClicked = False
    mPressed = False
    current_time = datetime.now()
    pos = (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mouseClicked = True
        elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
        elif event.type == pygame.KEYUP:
            if pressed[pygame.K_m]:
                mPressed = True
        elif event.type == pygame.QUIT:
            state = QUIT_STATE

    #State Selection
    if state == MENU_STATE:
        state = menu_state(screen, tnrMenuFont, tnrLargeFont, pos, mouseClicked)
    elif state == CREATE_GAME_STATE:
        pass
    elif state == GAME_STATE:
        current_color, numberOfTurnsSkipped = game_state(board, screen, tnrMediumFont, current_color, pos, numberOfTurnsSkipped, mouseClicked)
        if mPressed:
            state = MENU_MIDGAME_STATE
    elif state == MENU_MIDGAME_STATE:
        state = mid_game_menu_state(screen, tnrMenuFont, tnrLargeFont, pos, mouseClicked)
    elif state == RESTART_GAME_STATE:
        pass
    elif state == INFO_STATE:
        pass
    elif state == CREDITS_STATE:
        pass
    elif state == QUIT_STATE:
        running = False
    else:
        print("State Error.")
        state = QUIT_STATE

    #Timer to Break out from Program if idle for too long
    if mouseClicked:
        end_time = datetime.now() + timedelta(seconds=TIME_IDLE_QUIT)
    elif current_time >= end_time:
        state = QUIT_STATE

    pygame.display.flip()
    clock.tick(FPS) 

pygame.quit()