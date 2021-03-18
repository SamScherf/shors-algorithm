"""
file: factor.py

This file is the interactive part that allows the user
to enter numbers to factor with shors and perform various
actions. The bulk of the processing in then done by
functions implemented in classical.py and quantum.py
"""

# Import required libraries
import math

# Import actions
from classical import save_circut, run_shors

def main():
    """
    This function handles the flow of collecting a factor, guess,
    and action from the user then calling the action function
    """

    # Initialize dict of actions
    initialize_actions()

    # Get number to factor
    N = get_number_to_factor()

    # Get random guess
    a = get_guess(N)

    # Get action
    action = get_action(N)

    # Do action
    ACTIONS[action][1](a, N)



def initialize_actions():
    """
    This function creates a global dictionary of possible 
    actions with the value being a tuple where the first
    entry is a description of the action and the second
    is the function controlling the action.
    """

    global ACTIONS 
    ACTIONS = {1: ("Export circuit", save_circut), 2: ("Factor number", run_shors)}


def get_number_to_factor():
    """ 
    This function prompts the user for a natural
    number to factor
    """

    # Ask user for number
    user_input = input("What number would you like to factor? ")

    # Check if input is natural number
    if not user_input.isdigit() or int(user_input) == 0:
        print("Please enter a natural number to factor")
        user_input = get_number_to_factor()

    # Return
    return int(user_input)


def get_guess(N):
    """
    This function gets a guess from the user to run 
    shor's algorithm. If the guess does not require shor's algorithm,
    the function prompts the user for a different guess
    """

    # Ask user for number
    user_input = input("Guess a random number: ")

    # Check if user input is natural number
    if not user_input.isdigit() or int(user_input) == 0:
        print("Please enter a natural number as your guess")
        user_input = get_guess(N)

    # Convert guess into int
    a = int(user_input)

    # Check for gcd
    GCD = math.gcd(N,a)
    if GCD != 1:
        print(str(GCD) + " is a factor of both " + str(N) + " and " + str(a) + " so Shor's algorithm is not necessary")
        a = get_guess(N)

    # Return
    return a

def get_action(N):
    """
    This function prompts the user for what action they would like 
    to do from the global action dictionary
    """

    # Print section header
    print("What would you like to do?")

    # Print each option
    for key in ACTIONS: 
        print(str(key) + ". " + ACTIONS[key][0])

    # Prompt for action
    user_input = input("Type number: ")

    # Check if input is valid
    if not user_input.isdigit():
        print("Please just enter the number")
        user_input = get_action(N)

    # Convert input to action id
    action = int(user_input)

    # Check if action is valid
    if action not in ACTIONS:
        print("Please choose from the above list")
        user_input = get_action(N)

    # Check if user is trying to factor something other than 15
    if (action == 2 and N != 15):
        print("Sorry, this function can only factor 15 currently")
        action = get_action(N)

    # Return action
    return action


# Boilerplate
if __name__ == "__main__":
    main()
