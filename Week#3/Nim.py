"""
A simple Monte Carlo solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game
"""

import random
import codeskulptor
codeskulptor.set_timeout(20)

MAX_REMOVE = 3
TRIALS = 10000

def evaluate_position(num_items):
    """
    Monte Carlo evalation method for Nim
    """
    
    # Insert your code here
    move_list = [1, 2, 3]
    win_rate = []
    
    for val in move_list:
        comp_win = 0
        count = 0
        for dummy_iter in range(TRIALS):
            dummy_item = num_items - val
        
        
            while dummy_item > 0:
                new_mv = (random.randrange(MAX_REMOVE)+1)
            
                dummy_item -= new_mv
            
                count += 1
        
            if count % 2 == 0 and dummy_item <=0 :
                comp_win += 1

        win_rate.append(comp_win)
    max_val = max(win_rate)    
    for idx, val in enumerate(win_rate):
        if val == max_val:
            best_move = idx+1
        
    return best_move


def play_game(start_items):
    """
    Play game of Nim against Monte Carlo bot
    """
    
    current_items = start_items
    print "Starting game with value", current_items
    while True:
        comp_move = evaluate_position(current_items)
        current_items -= comp_move
        print "Computer choose", comp_move, ", current value is", current_items
        if current_items <= 0:
            print "Computer wins"
            break
        player_move = int(input("Enter your current move"))
        current_items -= player_move
        print "Player choose", player_move, ", current value is", current_items
        if current_items <= 0:
            print "Player wins"
            break

play_game(21)
        