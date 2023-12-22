import pygame
from datetime import datetime, timedelta

#COLORS
BOARD_GREEN = (29, 171, 72)
LIGHT_BOARD_GREEN = (31, 184, 130)
BACKGROUND_PURPLE = (91, 132, 199)
BORDER_RED = (120, 16, 28)
LINE_THICKNESS = 2


#DIMENSIONS
#Screen
SCREEN_DIMENSIONS = (1280, 720)

#Board
BOARD_EDGE_RADIUS = 5
BOARD_DIMENSIONS = (648, 648)
BOARD_START = (316, 36)
BORDER_THICKNESS = 5

#Text
TEXT_LOCATION = (35, 20)
BLACK_SCORE_LOCATION = (100, 625)
WHITE_SCORE_LOCATION = (1075, 625)

#Pieces
PIECE_OFFSET = 10
PIECE_RADIUS = (BOARD_DIMENSIONS[0] / 16) - PIECE_OFFSET
FIRST_PIECE = (BOARD_START[0] + PIECE_RADIUS + PIECE_OFFSET, BOARD_START[1] + PIECE_RADIUS + PIECE_OFFSET)
NEXT_PIECE_OFFSET = PIECE_OFFSET * 2 + PIECE_RADIUS  * 2
PIECE_BORDER_THICKNESS = 2

#OTHER
TIME_IDLE_QUIT = 300 #Seconds
FPS = 100 #Frames Per Second

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


#Create Board and Setup Starting Pieces. 1 Stands for White, 2 Stands for Black.
board = [[0 for i in range(8)] for j in range(8)]
board[3][3] = 1
board[4][4] = 1
board[3][4] = 2
board[4][3] = 2

current_color = 2 #Represents Black
numberOfTurnsSkipped = 0 #If gets to two and the timer passes, end game.
end_time = 0 #For when the game ends.

#Pygame Initialization
pygame.init()
statusFont = pygame.font.SysFont('Times New Roman', 25)
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Othello")
clock = pygame.time.Clock()
running = True


while running:
    mouseClicked = False
    current_time = datetime.now()
    pos = (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mouseClicked = True
        elif event.type == pygame.QUIT:
            running = False

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
    screen.fill(BACKGROUND_PURPLE)

    #Put Turn Text
    if numberOfTurnsSkipped == 0:
        color_word = 'White'
        if current_color == 2:
            color_word = 'Black'
        textSurface = statusFont.render(color_word + "'s Turn to Move.", False, 'black')
        screen.blit(textSurface, TEXT_LOCATION)

    elif numberOfTurnsSkipped >= 2:
        
        whiteCount, blackCount = count_pieces(board)
        if whiteCount > blackCount:
            message = "Game Over. White Won!"
        elif blackCount > whiteCount:
            message = "Game Over. Black Won!"
        else:
            message = "Game Over. It was a Tie."

        textSurface = statusFont.render(message, False, 'black')
        screen.blit(textSurface, TEXT_LOCATION)

    #Put Score Text
    whiteCount, blackCount = count_pieces(board)
    textSurface = statusFont.render(f"White: {whiteCount}", False, 'black')
    screen.blit(textSurface, WHITE_SCORE_LOCATION)
    textSurface = statusFont.render(f"Black: {blackCount}", False, 'black')
    screen.blit(textSurface, BLACK_SCORE_LOCATION)

    #Draw the Board
    pygame.draw.rect(screen, BOARD_GREEN, (BOARD_START, BOARD_DIMENSIONS), border_radius = BOARD_EDGE_RADIUS) 

    #Highlight Possible Moves
    for i, j in moveList:
        center = get_piece_location(i, j)
        pygame.draw.rect(screen, LIGHT_BOARD_GREEN, ((center[0] - NEXT_PIECE_OFFSET / 2, center[1] - NEXT_PIECE_OFFSET / 2), (NEXT_PIECE_OFFSET, NEXT_PIECE_OFFSET)))

    #Draw the Lines Around the Board
    pygame.draw.rect(screen, "black", (BOARD_START, (BOARD_DIMENSIONS[0] + BORDER_THICKNESS, BOARD_DIMENSIONS[1] + BORDER_THICKNESS)), 
                    border_radius = BOARD_EDGE_RADIUS, width = BORDER_THICKNESS)

    line_offset = NEXT_PIECE_OFFSET
    for i in range(7):
        pygame.draw.line(screen, "black", (BOARD_START[0] + line_offset, BOARD_START[1]), 
        (BOARD_START[0] + line_offset, BOARD_START[1] + BOARD_DIMENSIONS[1]), width = LINE_THICKNESS)
        pygame.draw.line(screen, "black", (BOARD_START[0], BOARD_START[1] + line_offset), 
        (BOARD_START[0] + BOARD_DIMENSIONS[0], BOARD_START[1] + line_offset), width = LINE_THICKNESS)
        
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
     
    pygame.display.flip()
    clock.tick(FPS)
    
    #Timer to Break out from Program
    if numberOfTurnsSkipped == 2:
        end_time = datetime.now() + timedelta(seconds=TIME_IDLE_QUIT)
    if numberOfTurnsSkipped >= 2 and current_time >= end_time:
        break

pygame.quit()