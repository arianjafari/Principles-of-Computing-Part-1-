"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 50         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    This function takes the current board and the nest players to move
    then it playes a move randomly and switches the player alternately
    """
    winner = board.check_win()
    
    
    if winner == None:
        
       
        empty_squares = board.get_empty_squares()
        new_move = empty_squares[random.randrange(len(empty_squares))]
        board.move(new_move[0], new_move[1], player)
        player = provided.switch_player(player)
        mc_trial(board, player)

def mc_update_scores(scores, board, player):
    """
    This function gets a completed board, the machine player, and
    the scores will be updated based on the completed board
    """
    board_dim = board.get_dim()
    
    
    winner = board.check_win()
    if winner == None or winner == provided.DRAW:
        return
    
    if winner == player:
        match_score = SCORE_CURRENT
        other_score = -1* SCORE_OTHER
    else:
        match_score = -1* SCORE_CURRENT
        other_score = SCORE_OTHER
        
        
    for row in range(board_dim):
        for col in range(board_dim):
            
            square_status = board.square(row, col)
            
            if square_status == player:
                scores[row][col] += match_score
            elif square_status == provided.switch_player(player):
                scores[row][col] += other_score
                
                

def get_best_move(board, scores):
    """
    This function takes a board and its corresponding score
    and then return an empty tupil as the best move based on the
    maximum scores among empty squares
    """
    
    empty_squares = board.get_empty_squares()
    
    if len(empty_squares) == 0:
        return
    
    max_score = -float('Inf')
    
    for square in empty_squares:
        max_score = max(max_score, scores[square[0]][square[1]])
    
    max_empty_squares = []
    
    for square in empty_squares:
        if scores[square[0]][square[1]] == max_score:
            max_empty_squares.append(square)
    
    best_move = max_empty_squares[random.randrange(len(max_empty_squares))]
    return best_move
    
def mc_move(board, player, trials):
    """
    This function gets a board and machine player and the number of trials
    and return a move for the machine
    """
    board_dim = board.get_dim()
    scores = [[0 for dummy_row in range(board_dim)] for dummy_col in range(board_dim)]
    for dummy_iter in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
        
    return get_best_move(board, scores)
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
