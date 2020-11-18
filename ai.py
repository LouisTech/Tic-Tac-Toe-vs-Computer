from random import seed
from random import randint
"""
Contains the AI logic for the game
including the minimax algorithm
for the hardest setting


easy: random empty cell is chosen
medium: chooses randomly but will take the win if possible
hard: minimax (impossible to beat)
"""

seed(52)


def ai_move(board, diff):
    if diff == "easy":
        indicies = none_indicies(board)
        i = randint(0, len(indicies)-1)
        return indicies[i]


def none_indicies(board):
    indicies = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == None:
                indicies.append([i, j])
    print(indicies)
    return indicies


if __name__ == "__main__":
    print(
        ai_move([[None, "x", "o"], [None, "x", None], ["o", None, "o"]], "easy"))
