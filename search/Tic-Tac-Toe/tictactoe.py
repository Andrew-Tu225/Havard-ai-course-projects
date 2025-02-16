"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = 0
    O_count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == X:
                X_count += 1
            elif board[i][j] == O:
                O_count += 1
    if X_count > O_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                actions.append((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check horizontal
    for i in range(len(board)):
        j = 0
        if board[i][j] == board[i][j+1] == board[i][j+2] == X:
            return X
        elif board[i][j] == board[i][j+1] == board[i][j+2] == O:
            return O
    
    #check vertical
    for j in range(len(board)):
        i = 0
        if board[i][j] == board[i+1][j] == board[i+2][j] == X:
            return X
        elif board[i][j] == board[i+1][j] == board[i+2][j] == O:
            return O
        
    #check diagonal
    if board[0][0] == board[1][1] == board[2][2] == X or board[2][0] == board[1][1] == board[0][2] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O or board[2][0] == board[1][1] == board[0][2] == O:
        return O
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not any(EMPTY in row for row in board) or winner(board) is not None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def min_value(board):
    if terminal(board):
        return utility(board), None
    else:
        action = None
        score = math.inf
        for move in actions(board):
            v,m = max_value(result(board, move))
            if score > v:
                score = v
                action = move
                if v==-1:
                    return score,move
                
        return score, action
    
def max_value(board):
    if terminal(board):
        return utility(board), None
    else:
        action = None
        score = -math.inf
        for move in actions(board):
            v, m = min_value(result(board, move))
            if score < v:
                score = v
                action = move
                if v==1:
                    return score, move
        return score, action
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == X:
        score, action = max_value(board)
        return action
    else:
        score, action = min_value(board)
        return action