import pygame
import sys
import os
import traceback
from datetime import datetime, timedelta

#Importing Constants
from helper_files.constants import *

#Importing Helpers + AIs
from helper_files.helpers import *
from helper_files.ai_algorithms import algorithm_picker

#Logging Specifications
if LOG_LOCATION == LOG_TO_FILE:
    #Logging STDOUT to check for uncaught errors
    now = datetime.now()
    datetimestring = now.strftime("%Y%m%d-%H%M%S")
    orig_stdout = sys.stdout
    directory_exists = os.path.isdir("logs")
    if not directory_exists:
        os.mkdir("logs")

    #Remove log files
    files = [i for i in os.listdir('logs') if i[:11] != "othello_log"]
    if len(files) > 4:
        dateDict = {}
        dates = []
        for file in files:
            date = datetime.strptime(file[:-4], "%Y%m%d-%H%M%S")
            dateDict[file[:-4]] = file
            dates.append(date)
        for i in range(4):
            newest = max(dates)
            newStr = newest.strftime("%Y%m%d-%H%M%S")
            poppedFile = dateDict[newStr]
            dates.remove(newest)
            files.remove(poppedFile)
        for file in files:
            os.remove(f"logs/{file}") 

    f = open(f'logs/{datetimestring}.txt', 'w')
    sys.stdout = f


#STATES
#TODO: ADD A RESTART STATE WITHIN
def game_state(board, screen, font, color, pos, turns, mouseClicked, player, lastMove, log_file):
    #Assign inputs to state variables
    numberOfTurnsSkipped = turns 
    current_color = color
    player_name = player[0]
    player_color = player[1]

    #Gets all possible moves for the current color. Changes the color if no moves exist. 
    moveList, moveDict = all_moves(board, current_color)

    #Gets whether a current user can play
    user_can_play = can_play(current_color, player_name, player_color)
    move = lastMove
    gameEnded = False
    counted = count_pieces(board)
    totalMoves = counted[0] + counted[1] - 4

    if len(moveList) == 0:
        current_color = switch_colors(current_color)
        numberOfTurnsSkipped += 1
        if numberOfTurnsSkipped >= 2:
            gameEnded = True
        else:
            return current_color, numberOfTurnsSkipped, move, log_file
    else:
        numberOfTurnsSkipped = 0

    #Place a piece down.
    if mouseClicked and within_board(pos[0], pos[1]) and user_can_play and not gameEnded:
        x, y = pos
        x_coord = int((x - BOARD_START[0]) / NEXT_PIECE_OFFSET)
        y_coord = int((y - BOARD_START[1]) / NEXT_PIECE_OFFSET)

        if board[x_coord][y_coord] == 0 and (x_coord, y_coord) in moveList:
            #For Logs
            if totalMoves == 0:
                log_file = output_board(board, totalMoves, player, log_file)

            #Move Code
            move = (x_coord, y_coord)
            strCoords = str(x_coord) + str(y_coord)
            board[x_coord][y_coord] = current_color
            for i, j in moveDict[strCoords]:
                board[i][j] = current_color
            current_color = switch_colors(current_color)

            #For Logs
            log_file = output_board(board, totalMoves + 1, player, log_file)
    elif not user_can_play and not gameEnded and move[0] != -1:
        mover = algorithm_picker(board, moveList, moveDict, current_color, player_name)
        x_coord, y_coord = mover

        if board[x_coord][y_coord] == 0 and (x_coord, y_coord) in moveList:
            #For Logs
            if totalMoves == 0:
                log_file = output_board(board, totalMoves, player, log_file)

            #Move Code
            move = (x_coord, y_coord)
            strCoords = str(x_coord) + str(y_coord)
            board[x_coord][y_coord] = current_color
            for i, j in moveDict[strCoords]:
                board[i][j] = current_color
            current_color = switch_colors(current_color)

            #For Logs
            log_file = output_board(board, totalMoves + 1, player, log_file)
    elif move[0] == -1:
        move = (-2, -2)
    
    #Fill in the Background
    screen.fill(BACKGROUND_BLUE)

    #Put Turn Text
    if not gameEnded:
        color_word = 'White'
        if current_color == 2:
            color_word = 'Black'
        write_text(color_word + "'s Turn to Move.", screen, font, 'black', TURN_LOCATION)
    else:
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

    #Highlight Possible Moves and the Last Move
    if user_can_play:
        for i, j in moveList:
            center = get_piece_location(i, j)
            pygame.draw.rect(screen, LIGHT_BOARD_GREEN, ((center[0] - NEXT_PIECE_OFFSET / 2, center[1] - NEXT_PIECE_OFFSET / 2), (NEXT_PIECE_OFFSET, NEXT_PIECE_OFFSET)), border_radius = BOARD_EDGE_RADIUS)
        if move[0] != -1 and not gameEnded:
            center = get_piece_location(move[0], move[1])
            pygame.draw.rect(screen, BOARD_YELLOW, ((center[0] - NEXT_PIECE_OFFSET / 2, center[1] - NEXT_PIECE_OFFSET / 2), (NEXT_PIECE_OFFSET, NEXT_PIECE_OFFSET)), border_radius = BOARD_EDGE_RADIUS)
            
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

    return current_color, numberOfTurnsSkipped, move, log_file

def mid_game_menu_state(screen, regular_font, title_font, pos, mouseClicked):
    #Draw Background
    screen.fill(BACKGROUND_GREEN)

    #Title
    pygame.draw.rect(screen, TEXT_BOX_ORANGE, (tuple_op(MENU_TITLE_LOCATION_MM, TEXT_BOX_OFFSET, SUB_TUPLE), 
                MIDMENU_TITLE_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (tuple_op(MENU_TITLE_LOCATION_MM, TEXT_BOX_OFFSET, SUB_TUPLE), 
                    MIDMENU_TITLE_BOX), border_radius = TEXT_BOX_CORNER, width = TITLE_BORDER)
    write_text("In-Game Options", screen, title_font, "black", MENU_TITLE_LOCATION_MM)

    #Options (Back to Game, Home Menu, Exit)
    rg_top_left, rg_bot_right = create_box_color(screen, regular_font, "Resume Game", RG_LOCATION, RG_BOX, TEXT_BOX_GREEN)
    menu_tl, menu_br = create_box_color(screen, regular_font, "Back to Menu", MIDMENU_LOCATION, MIDMENU_BOX, TEXT_BOX_GREEN)
    quit_tl, quit_br = create_box_color(screen, regular_font, "Exit", MM_QUIT_LOCATION, QUIT_BOX, TEXT_BOX_GREEN)

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

    #Title
    pygame.draw.rect(screen, TEXT_BOX_ORANGE, (tuple_op(MENU_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                MENU_TITLE_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (tuple_op(MENU_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                MENU_TITLE_BOX), border_radius = TEXT_BOX_CORNER, width = TITLE_BORDER)
    write_text("OTHELLO", screen, title_font, "black", MENU_TITLE_LOCATION)

    #Options (New Game, Info, Credits, Exit)
    ng_top_left, ng_bot_right = create_box_color(screen, regular_font, "New Game", NG_LOCATION, NG_BOX, TEXT_BOX_GREEN)
    info_tl, info_br = create_box_color(screen, regular_font, "Information", INFO_LOCATION, INFO_BOX, TEXT_BOX_GREEN)
    cred_tl, cred_br = create_box_color(screen, regular_font, "Credits", CRED_LOCATION, CRED_BOX, TEXT_BOX_GREEN)
    quit_tl, quit_br = create_box_color(screen, regular_font, "Exit", QUIT_LOCATION, QUIT_BOX, TEXT_BOX_GREEN)

    #Option Logic
    if mouseClicked:
        if within_box(pos[0], pos[1], ng_top_left, ng_bot_right):
            return CREATE_GAME_STATE
        elif within_box(pos[0], pos[1], info_tl, info_br):
            return INFO_STATE
        elif within_box(pos[0], pos[1], cred_tl, cred_br):
            return CREDITS_STATE
        elif within_box(pos[0], pos[1], quit_tl, quit_br):
            return QUIT_STATE

    return MENU_STATE

def info_state(screen, text_font, menu_font, title_font, pos, mouseClicked):
    #Draw Background
    screen.fill(BACKGROUND_GREEN)

    #Title
    pygame.draw.rect(screen, TEXT_BOX_ORANGE, (tuple_op(INFO_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                INFO_TITLE_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (tuple_op(INFO_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                INFO_TITLE_BOX), border_radius = TEXT_BOX_CORNER, width = TITLE_BORDER)
    write_text("Information", screen, title_font, "black", INFO_TITLE_LOCATION)

    #Text
    write_text("Othello is a strategy game that involves flipping pieces.", screen, text_font, "black", INFO_TEXT_LOCATION)
    write_text("The person with the most remaining pieces at the end wins.", screen, text_font, "black", 
        tuple_op(INFO_TEXT_LOCATION, (-10, TEXT_OFFSET), ADD_TUPLE))
    write_text("Each person takes turn placing a piece, with black starting.", screen, text_font, "black",
        tuple_op(INFO_TEXT_LOCATION, (-5, 2*TEXT_OFFSET), ADD_TUPLE))
    write_text("A move consists of placing a piece such that a piece of the opposite ", screen, text_font, "black",
        tuple_op(INFO_TEXT_LOCATION, (-40, 3*TEXT_OFFSET), ADD_TUPLE))
    write_text("color lies in between your move and another one of your pieces.", screen, text_font, "black",
        tuple_op(INFO_TEXT_LOCATION, (-30, 4*TEXT_OFFSET), ADD_TUPLE))
    write_text("Then, all pieces inbetween will flip colors to the mover's side.", screen, text_font, "black",
        tuple_op(INFO_TEXT_LOCATION, (-20, 5*TEXT_OFFSET), ADD_TUPLE))
    write_text("In this game, all possible moves will be highlighted.", screen, text_font, "black",
        tuple_op(INFO_TEXT_LOCATION, (10, 6*TEXT_OFFSET), ADD_TUPLE))
    write_text("Press M when in game to access the in-game menu.", screen, text_font, "black",
        tuple_op(INFO_TEXT_LOCATION, (15, 7*TEXT_OFFSET), ADD_TUPLE))

    #Back to Menu
    back_tl, back_br = create_box_color(screen, menu_font, "Back", BACK_I_LOC, BACK_BOX, TEXT_BOX_GREEN)

    #Option Logic
    if mouseClicked and within_box(pos[0], pos[1], back_tl, back_br):
        return MENU_STATE

    return INFO_STATE

def credits_state(screen, text_font, menu_font, title_font, pos, mouseClicked):
    #Draw Background
    screen.fill(BACKGROUND_GREEN)

    #Title
    pygame.draw.rect(screen, TEXT_BOX_ORANGE, (tuple_op(CRED_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                CRED_TITLE_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (tuple_op(CRED_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                CRED_TITLE_BOX), border_radius = TEXT_BOX_CORNER, width = TITLE_BORDER)
    write_text("Credits", screen, title_font, "black", CRED_TITLE_LOCATION)

    #Text
    write_text("Created by Abhijay Achukola (abhijay_py).", screen, text_font, "black", CRED_TEXT_LOCATION)
    write_text("Inspired by Varun Asuri's Othello AI.", screen, text_font, "black", 
        tuple_op(CRED_TEXT_LOCATION, (25, TEXT_OFFSET), ADD_TUPLE))
    #Back to Menu
    back_tl, back_br = create_box_color(screen, menu_font, "Back", BACK_C_LOC, BACK_BOX, TEXT_BOX_GREEN)

    #Option Logic
    if mouseClicked and within_box(pos[0], pos[1], back_tl, back_br):
        return MENU_STATE
    return CREDITS_STATE

def create_game_state(board, screen, menu_font, title_font, pos, mouseClicked, boxesPicked):
    #Color Vars
    colors = [] #pvp, easy, med, hard, expert, black, white, start
    for i in range(9):
        if i in boxesPicked:
            colors.append(TEXT_BOX_YELLOW)
        else:
            colors.append(TEXT_BOX_GREEN)
    
    new_boxes_picked = boxesPicked

    #Draw Background
    screen.fill(BACKGROUND_BLUE)

    #Title
    pygame.draw.rect(screen, TEXT_BOX_ORANGE, (tuple_op(CG_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                CG_TITLE_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (tuple_op(CG_TITLE_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE), 
                CG_TITLE_BOX), border_radius = TEXT_BOX_CORNER, width = TITLE_BORDER)
    write_text("Create A New Game", screen, title_font, "black", CG_TITLE_LOCATION)


    write_text("Select a Difficulty:", screen, menu_font, "black", DIFF_S_LOCATION)
    pvp_tl, pvp_br = create_box_color(screen, menu_font, "Human", PVP_LOCATION, PVP_BOX, colors[0])
    easy_tl, easy_br = create_box_color(screen, menu_font, "Easy", EASY_LOCATION, EASY_BOX, colors[1])
    med_tl, med_br = create_box_color(screen, menu_font, "Medium", MEDIUM_LOCATION, MEDIUM_BOX, colors[2])
    hard_tl, hard_br = create_box_color(screen, menu_font, "Hard", HARD_LOCATION, HARD_BOX, colors[3])
    exp_tl, exp_br = create_box_color(screen, menu_font, "Expert", EXPERT_LOCATION, EXPERT_BOX, colors[4])
    
    write_text("Select a Color:", screen, menu_font, "black", COLOR_S_LOCATION)
    bl_tl, bl_br = create_box_color(screen, menu_font, "Black", BLACK_LOCATION, BLACK_BOX, colors[5])
    wh_tl, wh_br = create_box_color(screen, menu_font, "White", WHITE_LOCATION, WHITE_BOX, colors[6])

    star_tl, star_br = create_box_color(screen, menu_font, "Start", START_LOCATION, START_BOX, colors[7])
    back_tl, back_br = create_box_color(screen, menu_font, "Back", BACK_CG_LOC, BACK_CG_BOX, colors[8])
    new_player = ("player", 1)
    
    #Option Logic
    if mouseClicked:
        if within_box(pos[0], pos[1], pvp_tl, pvp_br):
            new_boxes_picked = select_box(boxesPicked, 0, "diff")
        elif within_box(pos[0], pos[1], easy_tl, easy_br):
            new_boxes_picked = select_box(boxesPicked, 1, "diff")
        elif within_box(pos[0], pos[1], med_tl, med_br):
            new_boxes_picked = select_box(boxesPicked, 2, "diff")
        elif within_box(pos[0], pos[1], hard_tl, hard_br):
            new_boxes_picked = select_box(boxesPicked, 3, "diff")
        elif within_box(pos[0], pos[1], exp_tl, exp_br):
            new_boxes_picked = select_box(boxesPicked, 4, "diff")
        elif within_box(pos[0], pos[1], bl_tl, bl_br):
            new_boxes_picked = select_box(boxesPicked, 5, "color")
        elif within_box(pos[0], pos[1], wh_tl, wh_br):
            new_boxes_picked = select_box(boxesPicked, 6, "color")
        elif within_box(pos[0], pos[1], star_tl, star_br):
            new_player = get_selections(boxesPicked)
            return GAME_STATE, new_player, new_boxes_picked
        elif within_box(pos[0], pos[1], back_tl, back_br):
            return MENU_STATE, new_player, new_boxes_picked
    
    return CREATE_GAME_STATE, new_player, new_boxes_picked

#Main Loop
def main():
    #Create Board and Setup Starting Pieces. 1 Stands for White, 2 Stands for Black.
    board = create_new_board()
    current_color = 2 #Represents Black
    numberOfTurnsSkipped = 0 #If gets to two and the timer passes, end game.
    end_time = datetime.now() + timedelta(seconds=TIME_IDLE_QUIT) #For when the game ends.
    state = MENU_STATE #Works with the States listed in Constants
    player = ("player", 1) #The opponent the user is playing
    boxes_selected = [] #Selected boxes in create game
    lastMove = (-1, -1) #The last move made.
    log_file = None #initialize log_file variable

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

        if state != GAME_STATE and state != MENU_MIDGAME_STATE:
            log_file = None

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
            board = create_new_board()
            current_color = 2
            lastMove = (-1, -1)
            state, player, boxes_selected = create_game_state(board, screen, tnrMenuFont, tnrLargeFont, pos, mouseClicked, boxes_selected)
        elif state == GAME_STATE:
            current_color, numberOfTurnsSkipped, lastMove, log_file = game_state(board, screen, tnrMediumFont, current_color, pos, 
                                                                        numberOfTurnsSkipped, mouseClicked, player, lastMove, log_file)
            if mPressed:
                state = MENU_MIDGAME_STATE
        elif state == MENU_MIDGAME_STATE:
            state = mid_game_menu_state(screen, tnrMenuFont, tnrLargeFont, pos, mouseClicked)
            if mPressed:
                state = GAME_STATE
        elif state == INFO_STATE:
            state = info_state(screen, tnrMediumFont, tnrMenuFont, tnrLargeFont, pos, mouseClicked)
        elif state == CREDITS_STATE:
            state = credits_state(screen, tnrMediumFont, tnrMenuFont, tnrLargeFont, pos, mouseClicked)
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

if __name__ ==  "__main__":
    try:
        main()
        print("No Errors.")
    except Exception as e:
        print(traceback.format_exc())
    
pygame.quit()
if LOG_LOCATION == LOG_TO_FILE:
    sys.stdout = orig_stdout
    f.close()