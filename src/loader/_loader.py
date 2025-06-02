from qiskit import qasm2
from src.dtos import QuantumCircuit
from src.models.gates import X, Hadamard, CNOT, CZ, X, Y, Z, S, T, Rx, Ry, Rz, Identity

class Loader:
    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def load_qasm2(circuit_file: str) -> QuantumCircuit:
        """
        Load a QASM2 file and map it to the custom QuantumCircuit structure.

        :param circuit_file: Path to the QASM2 file.
        :return: A QuantumCircuit object representing the circuit.
        """
        qs_circuit = qasm2.load(circuit_file)
        custom_circuit = QuantumCircuit()

        # Map Qiskit circuit to custom circuit
        for instruction in qs_circuit.data:
            gate_name = instruction.operation.name
            if gate_name == 'measure':
                # Skip measurement gates as they are not part of the circuit structure
                continue
            target_qubits = [qubit._index for qubit in instruction.qubits]
            params = {param.name: param for param in instruction.operation.params}

            # Add qubits and gates to the custom circuit
            for qubit in target_qubits:
                custom_circuit.add_qubit(qubit)
            custom_circuit.add_gate(gate_name, target_qubits, params)

        return custom_circuit

    @staticmethod
    def load_qasm3(circuit_file: str) -> QuantumCircuit:
        # Placeholder for future implementation
        raise NotImplementedError("QASM3 loading not implemented yet.")

    @staticmethod
    def load_ir(circuit_file: str):
        # Placeholder for future implementation
        raise NotImplementedError("IR loading not implemented yet.")
