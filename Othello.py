import pygame

#COLORS
BOARD_GREEN = (29, 171, 72)
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

#Pieces
PIECE_OFFSET = 10
PIECE_RADIUS = (BOARD_DIMENSIONS[0] / 16) - PIECE_OFFSET
FIRST_PIECE = (BOARD_START[0] + PIECE_RADIUS + PIECE_OFFSET, BOARD_START[1] + PIECE_RADIUS + PIECE_OFFSET)
NEXT_PIECE_OFFSET = PIECE_OFFSET * 2 + PIECE_RADIUS  * 2
PIECE_BORDER_THICKNESS = 2

#Get location of the a specified piece
def get_piece_location(x, y):
    return (FIRST_PIECE[0] + x * NEXT_PIECE_OFFSET, FIRST_PIECE[1] + y * NEXT_PIECE_OFFSET)

#Create Board and Setup Starting Pieces.
board = [[0 for i in range(8)] for j in range(8)]
board[3][3] = 1
board[4][4] = 1
board[3][4] = 2
board[4][3] = 2

pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Othello")
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_PURPLE)

    #Draw the Board and Lines on the Board
    pygame.draw.rect(screen, BOARD_GREEN, (BOARD_START, BOARD_DIMENSIONS), border_radius = BOARD_EDGE_RADIUS) 
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
     
    #pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    dt = clock.tick(100) / 1000

pygame.quit()