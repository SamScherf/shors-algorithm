"""
file: factor.py

This file factors numbers using shor's algorithm
"""

# Import required libraries
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import numpy as np


def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2,7,8,11,13]:
        raise ValueError("'a' must be 2,7,8,11 or 13")
    U = QuantumCircuit(4)        
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

    U.draw(output="mpl", filename="U.png")
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
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
    qc.draw(output="mpl", filename="dagger.png")
    qc.name = "QFT†"
    return qc


def main():
    # Specify variables
    n_count = 8  # number of counting qubits
    a = 7
    
    
    # Create QuantumCircuit with n_count counting qubits
    # plus 4 qubits for U to act on
    qc = QuantumCircuit(n_count + 4, n_count)
    
    # Initialise counting qubits
    # in state |+>
    for q in range(n_count):
        qc.h(q)
        
    # And ancilla register in state |1>
    qc.x(3+n_count)
    
    # Do controlled-U operations
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q), 
                 [q] + [i+n_count for i in range(4)])
    
    # Do inverse-QFT
    qc.append(qft_dagger(n_count), range(n_count))
   
    qc.draw(output="mpl", filename="circuit.png")

    # Measure circuit
    qc.measure(range(n_count), range(n_count))
    qc.draw(fold=-1)  # -1 means 'do not fold' 




# Boilerplate
if __name__ == "__main__":
    main()
