"""
file: classical.py

This file implements all the functions needed to interact with the quantum
circuits implemented in quantum.py and manage all the classical computations
needed to run shor's algorithm.
"""

# import math libraries
import math
from fractions import Fraction

# Import quantum circuits needed to run shors
from quantum import *


def save_circut(a, N):
    """
    This function is simply a classical wrapper
    to create and save a quantum circuit
    """
    # Create circuit
    qc = create_shors_circuit(a, N)

    # Draw circuit
    draw_circut(qc)



def run_shors(a, N):
    """
    This function handles the classical side
    of shors algorithm by running a simulation on the
    circuit
    """

    # Create circuit
    qc = create_shors_circuit(a, N)

    # Run circuit
    counts = run_simulator(qc) 
   
    # Save histogram of results
    save_histogram(counts) 

    # Get possible r's
    r_list = process_counts(counts)
    
    # Get the factor
    factor = get_factor(r_list, a, N)
    
    # Check if factor was found
    if factor != 0:
        # Print factor
        print(str(factor) + " is a factor of " + str(N) + "!")
    else:
        print("Sorry, this guess did not work. Please try another")



def process_counts(counts):
    """
    This function process's the measured bits to
    return a list of possible r values
    """

    # Initialize variables
    r_list = list()

    # Loop though outputs
    for output in counts:
            # Covert binary to decimal
            decimal = int(output, 2)

            # Get phase
            phase = decimal/(2**len(output))

            # Remove s
            r = remove_s(phase)

            # Add r to list
            r_list.append(r)

    # Return
    return r_list


def remove_s(phase):
    """
    This is a helper function used to by process_counts
    to remove the 's' factor in the measured phase.
    It does this by returning the denominator of the
    continued fraction generated by the float its given
    """

    # Turn into fraction
    fraction = Fraction(phase).limit_denominator(10)

    # Return denominator
    return fraction.denominator


def get_factor(r_list, a, N):
    """
    This function checks each r found by QPE
    to see if it can be used to find a factor of
    N. This function will return the factor if it is found
    otherwise it will return 0
    """

    # Clean list
    for r in r_list:
        # Check if r is odd
        if r % 2 == 1:
            # Remove if so
            r_list.remove(r)

    # Loop though possible r's
    for r in r_list:
        # Check for plus case
        GCD = math.gcd(int(a**(r/2)) + 1, N)
        if GCD != 1 and GCD < N:
            return GCD

        # Check for minus case
        GCD = math.gcd(int(a**(r/2)) - 1, N)
        if GCD != 1 and GCD < N:
            return GCD

    # Otherwise return 0
    return 0
