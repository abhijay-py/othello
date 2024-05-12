import random
import time
from helper_files.helpers import all_moves, min_max, count_pieces

boardHeuristic = [
    [500, -15, 10, 10, 10, 10, -15, 500],
    [-15, -15,  1,  1,  1,  1, -15, -15],
    [ 10,   1,  1,  1,  1,  1,   1,  10],
    [ 10,   1,  1,  1,  1,  1,   1,  10],
    [ 10,   1,  1,  1,  1,  1,   1,  10],
    [ 10,   1,  1,  1,  1,  1,   1,  10],
    [-15, -15,  1,  1,  1,  1, -15, -15],
    [500, -15, 10, 10, 10, 10, -15, 500]]

#Random Generator of Moves
def easy_algorithm(board, moveList, moveDict, current_color):
    return random.choice(moveList)

#Greedy Algorithm
def medium_algorithm(board, moveList, moveDict, current_color):
    maxLen = -1
    move = (0, 0)
    for i, j in moveList:
        moveKey = str(i) + str(j)
        removed = moveDict[moveKey]
        if len(removed) > maxLen:
            maxLen = len(removed)
            move = (i, j)
    return move

#Minimax Algorithm with Depth 2
def hard_algorithm(board, moveList, moveDict, current_color):
    return min_max(board, boardHeuristic, current_color, current_color, 2, True, 0, True)

#Minimax Algorithm with Depths of 3, 2, 5 in early, mid, and late game
def expert_algorithm(board, moveList, moveDict, current_color):
    count = count_pieces(board)
    empty = 64 - count[0] - count[1]
    depth = 5
    return min_max(board, boardHeuristic, current_color, current_color, depth, True, 0, True, -999999, 999999)

#Pick which algorithm to choose
def algorithm_picker(board, moveList, moveDict, current_color, algorithm_name):
    start = time.process_time()

    if algorithm_name == "easy":
        move = easy_algorithm(board, moveList, moveDict, current_color)
    elif algorithm_name == "medium":
        move = medium_algorithm(board, moveList, moveDict, current_color)
    elif algorithm_name == "hard":
        move = hard_algorithm(board, moveList, moveDict, current_color)
    elif algorithm_name == "expert":
        move = expert_algorithm(board, moveList, moveDict, current_color)
    else:
        print("Algorithm Choosing Error.")
        return None

    time_taken = time.process_time() - start

    if move not in moveList:
        print(f"Algorithm {algorithm_name} gave invalid move {move}.")
        return None
    
    if time_taken <= 1:
        time.sleep(1)

    return move