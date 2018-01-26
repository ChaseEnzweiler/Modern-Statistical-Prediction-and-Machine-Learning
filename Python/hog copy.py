"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled (capped at 11 - NUM_ROLLS).
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1============================================================================================

    sum_of_rolls = 0

    num_of_ones = 0

    for turn in range(0, num_rolls):   # generates one iteration for each dice

        value = dice()

        if value == 1:

            num_of_ones += 1

        else:

            sum_of_rolls = sum_of_rolls + value

    if num_of_ones != 0:

        return min(11 - num_rolls, num_of_ones)

    return sum_of_rolls

    # END PROBLEM 1 # completed============================================================================================


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2============================================================================================
    
    return max(opponent_score % 10, opponent_score // 10) + 1

    # END PROBLEM 2============================================================================================


# Write your prime functions here!

def is_prime(dice_score):
    """ Function that takes score from turn and returns boolean True if the score is prime

        >>> is_prime(9) 
        False
        >>> is_prime(1)
        False
        >>> is_prime(3)
        True

    """

    if dice_score == 2: #2 is the only even prime number
        return True

    if dice_score < 2 or dice_score % 2 == 0 : # even numbers(except 2) and numbers < 2 are not prime 
        return False

    for factor in range(3, dice_score - 1, 2): #checks for any odd factors 

        if dice_score % factor == 0: 

            return False

    return True

def next_prime(prime_num):
    """ takes a prime number and returns the next largest prime number

    >>> next_prime(7)
    11
    >>> next_prime(2)
    3
    """
    next_integer = prime_num + 1 

    while is_prime(next_integer) == False:

        next_integer += 1

    return next_integer


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2============================================================================================

    if num_rolls == 0: # chooses to roll no dice and use freebacon

        score = free_bacon(opponent_score)

    else:
        
         score = roll_dice(num_rolls, dice) # initial score from rolling the die

    if is_prime(score) == True: # hogtimus prime

        return next_prime(score)

    return score

    # END PROBLEM 2============================================================================================


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3============================================================================================
    
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided

    # END PROBLEM 3============================================================================================

def is_swap(score0, score1):
    """Returns whether one of the scores is double the other. Boolean
    """
    # BEGIN PROBLEM 4============================================================================================
    if (score0 / score1) == 2 or (score1/score0) == 2:
        return True
    else:
        return False
    # END PROBLEM 4============================================================================================

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5============================================================================================

    while (score0 < goal) and (score1 < goal): # exit loop when goal score is reached 

        if player == 0: 

            score0 = score0 + take_turn(strategy0(score0, score1), score1, dice = select_dice(score0, score1)) 

            if (score0 != 0) and (score1 != 0) and is_swap(score0, score1): # scores cant be zero or get division error

                place_hold0 = score0

                place_hold1 = score1

                score0 = place_hold1

                score1 = place_hold0


        else:

            score1 = score1 + take_turn(strategy1(score1, score0), score0, dice = select_dice(score1, score0))

            if (score0 != 0) and (score1 != 0) and is_swap(score1, score0): # scores cant be zero or get division error

                place_hold0 = score0

                place_hold1 = score1

                score0 = place_hold1

                score1 = place_hold0

        player = other(player)

    # END PROBLEM 5============================================================================================
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6============================================================================================

    test_score = 0

    while test_score < goal:

        test_opponent_score = 0

        while test_opponent_score < goal:

            check_strategy_roll(test_score, test_opponent_score, strategy(test_score, test_opponent_score))

            test_opponent_score += 1

        test_score += 1

    # END PROBLEM 6============================================================================================


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7============================================================================================

    def average(*args):

        sample = 0

        total = 0

        while sample < num_samples:

            total = total + fn(*args)

            sample += 1

        result = total / num_samples

        return result

    return average

    # END PROBLEM 7============================================================================================


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8============================================================================================

    previous = 0

    averaged_rolls = make_averaged(roll_dice)

    for num_rolls in range(1, 11): #iterates 1 to 10 

        current = averaged_rolls(num_rolls, dice)  

        maximum = max(previous, current)

        if maximum > previous:

            amount_of_die = num_rolls

        previous = maximum

    return amount_of_die

    # END PROBLEM 8============================================================================================


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9============================================================================================

    value_scored = free_bacon(opponent_score)

    if is_prime(value_scored):

        value_scored = next_prime(value_scored)

    if value_scored >= margin:

        return 0

    else:

        return num_rolls
    
    # END PROBLEM 9============================================================================================
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10============================================================================================

    value_scored = free_bacon(opponent_score)

    if is_prime(value_scored):

        value_scored = next_prime(value_scored)

    if value_scored >= margin:

        return 0

    elif ((score + value_scored) < opponent_score) and is_swap((score + value_scored), opponent_score):

        return 0

    else:

        return num_rolls

    # END PROBLEM 10============================================================================================
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    chooses to roll 4 dice when using a four sided dice and uses swap strategy 
    takes bigger risks by rolling more dice when losing by a lot and takes 
    smaller risks rolling less dice when close to 100 points

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11============================================================================================

    if opponent_score - score > 21:

        return swap_strategy(score, opponent_score, margin=20, num_rolls=8)

    if score >= 80:

        return swap_strategy(score, opponent_score, margin=9, num_rolls=4)

    if select_dice(score, opponent_score) == four_sided:

        return swap_strategy(score, opponent_score, margin=7, num_rolls=4)

    

    return swap_strategy(score, opponent_score, margin=10, num_rolls=6)


    # END PROBLEM 11============================================================================================
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()