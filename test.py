from qiskit import QuantumCircuit

qasm_string = """
OPENQASM 2.0;
include "stdgates.inc";
qreg q[2];
h q[0];
cx q[0], q[1];
"""

qc = QuantumCircuit.from_qasm_str(qasm_string)

# Iterate through the circuit's data (gates and qubit/classical bit mappings)
for instruction in qc.data:
    gate = instruction[0]  # Gate object
    qubits = instruction[1]  # List of Qubit objects
    clbits = instruction[2]  # List of Classical Bit objects

    gate_name = gate.name  # Gate name (e.g., 'h', 'cx')
    qubit_indices = [qc.find_bit(q).index for q in qubits]  # List of qubit indices
    clbit_indices = [qc.find_bit(c).index for c in clbits]  # List of clbit indices
    params = gate.params  # List of parameters

    print(
        f"Gate: {gate_name}, Qubits: {qubit_indices}, Params: {params}, Classical Bits: {clbit_indices}"
    )

    # Here, you would insert your own logic to process the gate information.
    # For example, you might create objects in your simulator's data structures
    # based on the extracted gate_name, qubit_indices, and params.
