from helper_files.helpers import all_moves

#Random Generator of Moves
def easy_algorithm(board, moveList, moveDict, current_color):
    return (0, 0)

#Greedy Algorithm
def medium_algorithm(board, moveList, moveDict, current_color):
    return (0, 0)

#? Algorithm
def hard_algorithm(board, moveList, moveDict, current_color):
    return (0, 0)

#Fully trained RL algorithm
def expert_algorithm(board, moveList, moveDict, current_color):
    return (0, 0)

#Pick which algorithm to choose
def algorithm_picker(board, moveList, moveDict, current_color, algorithm_name):
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