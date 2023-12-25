import random
import time
from helper_files.helpers import all_moves

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

#? Algorithm
def hard_algorithm(board, moveList, moveDict, current_color):
    return (0, 0)

#Fully trained RL algorithm
def expert_algorithm(board, moveList, moveDict, current_color):
    return (0, 0)

#Pick which algorithm to choose
def algorithm_picker(board, moveList, moveDict, current_color, algorithm_name):
    time.sleep(1)
    if algorithm_name == "easy":
        move = easy_algorithm(board, moveList, moveDict, current_color)
    elif algorithm_name == "medium":
        move = medium_algorithm(board, moveList, moveDict, current_color)
    elif algorithm_name == "hard":
        move = hard_algorithm(board, moveList, moveDict, current_color)
    elif algorithm_name == "expert":
        move = expert(board, moveList, moveDict, current_color)
    else:
        print("Algorithm Choosing Error.")
        return None

    if move not in moveList:
        print(f"Algorithm {algorithm_name} gave invalid move {move}.")
        return None
    
    return move