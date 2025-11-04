# Simon's Problem test
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Secret string s (hidden bitstring)
s = '110'
n = len(s)

# Oracle construction
def simon_oracle(s):
    n = len(s)
    qc = QuantumCircuit(2*n)
    # Copy x register into y register where s_i = 0
    for i in range(n):
        if s[i] == '0':
            qc.cx(i, n+i)
    # Add XOR with s where s_i = 1
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n-1)  # XOR pattern ensures f(x)=f(x⊕s)
    return qc

# Simon's algorithm circuit
qc = QuantumCircuit(2*n, n)
qc.h(range(n))                   # Hadamards on input register
qc.compose(simon_oracle(s), inplace=True)
qc.h(range(n))                   # Second layer of Hadamards
qc.measure(range(n), range(n))   # Measure input register

# Simulation
sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1024).result()
counts = result.get_counts()

print("Measurement results:")
print(counts)

plot_histogram(counts)
plt.title("Simon's Algorithm Results")
plt.show()
