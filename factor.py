"""
file: factor.py

This file factors numbers using shor's algorithm
"""

# Import required libraries
from qiskit import QuantumCircuit, transpile, execute, Aer, assemble
from qiskit.visualization import plot_histogram
from qiskit.visualization.timeline import IQXSimple
import numpy as np
import math
from qiskit.circuit.library import QFT
from fractions import Fraction

def main():

    # Get number to factor
    N = get_number_to_factor()

    # Get random guess
    a = get_random_number(N)

    # Get action
    action = get_action(N)

    # Create circuit
    qc = create_shors_circuit(N, a)

    # Do action
    if action == 1:
        # Draw circuit
        qc.draw(output="mpl", filename="circuit.png", fold=-1)
    if action == 2:
        # Run circuit
        counts = run_simulator(qc) 
        
        # Save histogram
        plot_histogram(counts, title="Results", figsize=(9, 12)).savefig("histogram.png")

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





def get_factor(r_list, a, N):

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



def process_counts(counts):

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
    # Turn into fraction
    fraction = Fraction(phase).limit_denominator(10)

    # Return denominator
    return fraction.denominator



def run_simulator(qc):
    qasm_sim = Aer.get_backend('qasm_simulator')
    t_qc = transpile(qc, qasm_sim)
    qobj = assemble(t_qc)
    results = qasm_sim.run(qobj).result()

    # Return counts
    return results.get_counts()

def get_action(N):

    # Ask for action
    print("What would you like to do?")
    print("1. Export circuit")
    print("2. Factor number")
    action = int(input("Type number: "))

    # Check if valid action
    if (action == 2 and N != 15):
        print("Sorry, this function can only factor 15 currently")
        action = get_action(N)

    # Return action
    return action



def create_shors_circuit(N, a):

    # Get number of bits to represent N
    N_bits = math.ceil(np.log2(N+1))

    # Create list of counting bits
    counting_qubits = list()
    for i in range(2*N_bits):
        counting_qubits.append(i)

    # Create list of input bits
    input_qubits = list()
    for i in range(2*N_bits, 3*N_bits):
        input_qubits.append(i)

    # Initialize circuit
    qc = initialize_circuit(counting_qubits, input_qubits)

    # Add U gates
    for qubit in counting_qubits:
        power = 2**qubit
        qc.append(U_gate(a, power, N), [qubit] + input_qubits)
  

    # Add inverse QFT
    qc.append(qft_dagger(len(counting_qubits)), counting_qubits)

    # Add measuring devices
    for qubit in counting_qubits:
        bit = qubit
        qc.measure(qubit, bit)

    # Return circuit
    return qc



def get_random_number(N):
    
    # Ask user for number
    a = int(input("Guess a random number: "))

    # Check for gcd
    GCD = math.gcd(N,a)
    if GCD != 1:
        print(str(GCD) + " is a factor of both " + str(N) + " and " + str(a) + " so Shor's algorithm is not necessary")
        a = get_random_number(N)

    # Return
    return a


def get_number_to_factor():
    
    # Ask user for number
    N = int(input("What number would you like to factor? "))

    # Return
    return N



def initialize_circuit(counting_qubits, input_qubits):
    # Initialize circuit
    qc = QuantumCircuit(len(counting_qubits) + len(input_qubits), len(counting_qubits))

    # Add haramod to counting bits
    for qubit in counting_qubits:
        qc.h(qubit)

    # Set input to |1>
    qc.x(input_qubits[len(input_qubits)-1])

    # Return
    return qc



def U_gate(a, power, N):

    # Get number of bits to represent N
    N_bits = math.ceil(np.log2(N+1))

    # Initialize gate
    U = QuantumCircuit(N_bits)

    # Create U gate for N=15
    for iteration in range(power):
        if a in [2,13]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [7,8]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a == 11:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)

    # Convert circuit to gate with one control
    U = U.to_gate()
    U.name = "(" + str(a) + "^" + str(power) + " mod " + str(N) + ")"
    c_U = U.control()

    # Return gate
    return c_U

def qft_dagger(n):
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc



# Boilerplate
if __name__ == "__main__":
    main()
