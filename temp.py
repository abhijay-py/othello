#Switches between colors
def switch_colors(color):
    if color == 1:
        return 2
    return 1
#Checks if board coordinates are located within the board
def within_board_coords(x, y):
    return x <= 7 and x >= 0 and y <= 7 and y >= 0

def try_remove(array, item):
    try:
        array.remove(item)
    except:
        pass
    return array
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
                    if x == 5 and y == 4:
                        print(board[x+i][y+j], (i, j))
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

board = [[0 for i in range(8)] for j in range(8)]
board[3][3] = 1
board[4][4] = 1
board[3][4] = 2
board[4][3] = 2

current_color = 2 #Represents Black

listed, dicted = all_moves(board, current_color)
print(listed)
print(dicted)