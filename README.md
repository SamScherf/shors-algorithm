# Shor's Algorithms
This is some Qiskit code built as a learning tool to show how Shor's algorithm works. Given the scope
of the project and its purpose as an introductory learning tool, the function is only able to actually factor
the number 15 as implementing an operator for any general N is a very complex task that theorists are still
discovering new ways to do.


## Usage
Simply run the main python file

```
python main.py
````

Upon running the program, the user will be prompted for a number to factor and another random integer
to use as the "guess". If desired, the user can then simulate that hardware using Qiskit's Aer simulator
which will return a factor and print a histogram of what a quantum computer would have measured. The user
can also choose to simply print the circuit and see how it would look for integers != 15

## Implementation

The file which the user runs (main.py) is mostly a wrapper file which just collects input from the user
and verifies that the input is valid. Upon collecting all the data, the file makes use of the functions
implemented in "classical.py". Classical.py implements all the classical functions necessary to run Shor's algorithm
(hence the name) and makes use of "quantum.py" for all the Qiskit code and quantum computing. Quantum.py, as you
would expect, implements the quantum circuits required for Shor's algorithm.

### Nitty-Gritty

At it's core, Shor's algorithm works by turning the problem of factoring a number into a period finding problem then
involving quantum phase estimation (QPE) to solve for said period and thereby factor the number. To do this, Shor's algorithm
first and foremost makes use of two import math theorems:  

1. The Euclidean Algorithm (which provides a classical algorithm to find the GCD of two natural numbers)
2. Euler's Theorem (which says that a^x = 1 (mod N) for some integer x if a and N are co-prime)

The second of thermos, Euler's Theorem, is particularly useful in that by simply subtracting 1 and factoring:  

a^x = 1 (mod N)  
a^x - 1 = 0 (mod N)  
(a^(x/2) - 1) * (a^(x/2) + 1) = 0 (mod N)  

We are able to see that finding an integer x such that a^x = 1 (mod N), we will have a high likelihood of "guessing" a
factor of N. This is turned into a period finding problem by simply acknowledging that a^0 = 1 (mod N) is a trivial solution
to this problem and that since (mod N) makes the function periodic, we can simply add the period (which we will call r) to
the 0 to get a non trivial solution:  

a^0 = 1 (mod N) and a^0 = a^(0+r) (mod N) therefore  
a^r = 1 (mod N)  


## Dependencies
This program requires the Qiskit, matplotlib, and pylatexenc which can all be installed with the following command

```
pip install qiskit matplotlib pylatexenc
```
