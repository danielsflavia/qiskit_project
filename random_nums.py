from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator

# function that creates a 1-qubit quantum random generator
def create_quantum_bit_circuit():
    qr = QuantumRegister(1) # quantum register with 1 qubit
    cr = ClassicalRegister(1)   # classical register with 1 classical bit
    circuit = QuantumCircuit(qr, cr)    # quantum circuit that uses both registers
    circuit.h(qr[0])    #  puts a Hadamard gate to the qubit (superposition)
    circuit.measure(qr[0], cr[0])   # puts qubit into the classical bit (collabses to either 0 or 1)
    return circuit

# function that xreates a 8-bit quantum generator
def create_8bit_random_number_circuit():
    qr = QuantumRegister(8)      # 8 qubits
    cr = ClassicalRegister(8)    # 8 classical bits

    qc = QuantumCircuit(qr, cr)

    qc.h(range(8))               # put ALL qubits into superposition
    qc.measure(range(8), range(8))  # measure all 8 qubits

    return qc

## 1-bit generator
simulator = AerSimulator()  # simulator object

circuit = create_quantum_bit_circuit()  # call function
circuit = transpile(circuit, simulator) # optimize circuit to make it compatilble with the simulator

job = simulator.run(circuit, shots=10)  # run circuit 10 times on simulator
result = job.result()

print("Random bit counts:  ", result.get_counts())


## 8 but generator
qc_8bit = create_8bit_random_number_circuit()
qc_8bit = transpile(qc_8bit, simulator)

job2 = simulator.run(qc_8bit, shots=1)
result2 = job2.result()

# get the single binary string result
bitstring = list(result2.get_counts().keys())[0]

# qiskit outputs bits reversed (little endian), so flip
bitstring = bitstring[::-1]

# convert to normal integer
number = int(bitstring, 2)

print("Random number:", number)
