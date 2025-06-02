from typing import List, Dict

class QuantumCircuit:
    def __init__(self):
        self.qubits: List[int] = []  # List of qubit indices
        self.gates: List[Dict[str, any]] = []  # List of gates with their properties

    def add_qubit(self, qubit_index: int):
        """Add a qubit to the circuit."""
        if qubit_index not in self.qubits:
            self.qubits.append(qubit_index)

    def add_gate(self, gate_name: str, target_qubits: List[int], params: Dict[str, any] = None):
        """Add a gate to the circuit."""
        self.gates.append({
            "name": gate_name,
            "targets": target_qubits,
            "params": params or {}
        })

    def __repr__(self):
        return f"QuantumCircuit(qubits={self.qubits}, gates={self.gates})"

