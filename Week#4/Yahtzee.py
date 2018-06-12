"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)





def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    
    hand_set = list(set(list(hand)))
    
        
    maximum = 0 
    for val in hand_set:
        max_val = 0
        for h_val in hand:
            if h_val == val:
                max_val += val
        maximum = max(max_val,maximum)        
    
    return maximum            
    
    


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [(idx+1) for idx in range(num_die_sides)]
    
    remaining_hand =  list(gen_all_sequences(outcomes, num_free_dice))
    
    prob = (1.0/num_die_sides)**num_free_dice
    
    held_dice = list(held_dice)
    
    expect_value = 0
    
    for seq in remaining_hand:
        
        hand = held_dice + list(seq)
        expect_value += prob*score(hand)
    
    return expect_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    sorted_hand = sorted(hand)
     
    all_hands = [hand]
    
    for idx in range(0,len(hand)):
        
        all_hands += list(gen_all_sequences(sorted_hand, idx))
        
    
    
    
    for idx, value  in enumerate(all_hands):
        all_hands[idx] = tuple(sorted(value))
    
    all_hands = set(all_hands)
    
    
    frequency = [0 for dummy_value in hand]
    
    
    for idx in range(len(hand)):
        for val in hand:
            if val == hand[idx]:
                frequency[idx] += 1
               
    
    for idx,hand_val in enumerate(hand):
        
        for all_val in list(all_hands):
            count = 0 
            for tuple_val in all_val:
                
                if tuple_val == hand_val:
                    count += 1
            if count > frequency[idx]:
                all_hands.remove(all_val)
    
    return all_hands



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    all_hands = list(gen_all_holds(hand))
    best_strategy = [0,0]
    for val in all_hands:
        num_free_dice = len(hand) - len(val)
        exp_val = expected_value(val, num_die_sides, num_free_dice)
        print best_strategy
        if exp_val > best_strategy[0]:
            best_strategy[0] = exp_val
            best_strategy[1] = val
        
        
    return tuple(best_strategy)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (3, 3, 3, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()

#score((3,3,3,6,6))
#expected_value((1,1), 6, 2)
#gen_all_holds((1,1,6))
#strategy((1,1,6), 6)
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



