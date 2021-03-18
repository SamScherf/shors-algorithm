"""
file: quantum.py

This file implements all the functions need to print out a quantum 
circuit capable of running shor's algorithm or actually running it on
the number 15
"""

# Import Qiskit libraries
from qiskit import QuantumCircuit, transpile, execute, Aer, assemble
from qiskit.visualization import plot_histogram
from qiskit.visualization.timeline import IQXSimple
from qiskit.circuit.library import QFT

# Import math libraries
import numpy
import math

def create_shors_circuit(a, N):
    """
    This function creates Shors circuit which is essentially
    just quantum phase estimation with U|y> = |ay mod N>
    """

    # Get number of bits to represent N
    N_bits = int(numpy.ceil(numpy.log2(N+1)))

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


def initialize_circuit(counting_qubits, input_qubits):
    """
    This is a helper function for create_shors_circuit which just initializes
    the circuit with the proper number of quantum and classical channels and
    sets all the qubits to the proper starting position
    """

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
    """
    This function implements the U operator U|y> = |ay mod 15>.
    Ideally this function would implement U|y> = |ay mod N> but given
    the complexity of such a gate, it currently only supports N=15.
    Other N's may be enter but the gate will no longer work
    properly and will only be useful in visually demonstrating how such
    a gate would be used
    """

    # Get number of bits to represent N
    N_bits = int(numpy.ceil(numpy.log2(N+1)))

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
    U = U.control()

    # Return gate
    return U


def draw_circut(qc):
    """
    This function simply saves a given circuit in the working directory
    with the name "circuit.png"
    """

    # Draw circuit
    qc.draw(output="mpl", filename="circuit.png", fold=-1)


def save_histogram(counts):
    """
    This function simply saves a history in the working directory
    with the name "histogram.png" of some given counts
    """

    # Save histogram
    plot_histogram(counts, title="Results", figsize=(9, 12)).savefig("histogram.png")


def run_simulator(qc):
    """
    This function returns a simulation of a given circuit
    and returns the results
    """

    # Get simulation backend
    simulator = Aer.get_backend('qasm_simulator')

    # Transpile circuit
    transpiled_circuit = transpile(qc, qasm_sim)
    
    # Assemble and run circuit
    assembled_circuit = assemble(t_qc)
    results = qasm_sim.run(assembled_circuit).result()

    # Return counts
    return results.get_counts()



def qft_dagger(n):
    """
    This is the qft dagger function provided by the Qiskit documentation.
    """

    # Initialize circuit 
    qc = QuantumCircuit(n)
    
    # Implement QFT
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-numpy.pi/float(2**(j-m)), m, j)
        qc.h(j)

    # Name gate
    qc.name = "QFT†"

    # Return gate
    return qc
