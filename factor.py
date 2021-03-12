"""
file: factor.py

This file factors numbers using shor's algorithm
"""

# Import required libraries
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram


def main():
    # Use Aer's qasm_simulator
    backend = Aer.get_backend('qasm_simulator')

     # Initialize constants
    qubits = 2
    classical_bits = 2

    # Create the circuit
    circuit = create_circuit(qubits, classical_bits)

    # Draw the circuit
    circuit.draw(output='mpl', filename="circuit.png")

    # Execute the circuit on the backend
    job = execute(circuit, backend, shots=1000)
    
    # Grab results from the job
    result = job.result()
    
    # Returns counts
    counts = result.get_counts(circuit)
       
    # Plot histogram of results
    plot_histogram(counts, color='midnightblue', title="Histogram").savefig("histogram.png")



def create_circuit(qubits, classical_bits):
    """
    This function creates the quantum circuit needed to run
    shor's algorithm
    """

    # Create a Quantum Circuit
    circuit = QuantumCircuit(qubits, classical_bits)
    
    # Add a H gate on qubit 0
    circuit.h(0)
    
    # Add a CX gate on control qubit 0 and target qubit 1
    circuit.cx(0, 1)
    
    # Add a measuring device
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    
    # Return the circuit
    return circuit


# Boilerplate
if __name__ == "__main__":
    main()
