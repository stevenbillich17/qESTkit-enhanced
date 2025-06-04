from typing import List, Dict

from sympy.strategies.core import switch

from src.models.Gate import Gate
from src.models.gates import X, Hadamard, CNOT, CZ, X, Y, Z, S, T, Rx, Ry, Rz, Identity


class QuantumCircuit:
    def __init__(self):
        self.qubits: List[int] = []  # List of qubit indices
        self.gates: List[Gate] = []  # List of gates with their properties

    def add_qubit(self, qubit_index: int):
        """Add a qubit to the circuit."""
        if qubit_index not in self.qubits:
            self.qubits.append(qubit_index)

    def add_gate(
        self, gate_name: str, target_qubits: List[int], params: Dict[str, any] = None
    ):
        """Add a gate to the circuit."""
        if not isinstance(target_qubits, list):
            raise TypeError("target_qubits must be a list of integers.")
        if gate_name not in [
            "X",
            "Hadamard",
            "H",
            "h",
            "CNOT",
            "cx",
            "CZ",
            "Y",
            "Z",
            "S",
            "T",
            "Rx",
            "Ry",
            "Rz",
            "Identity",
        ]:
            raise ValueError(
                f"Unsupported gate: {gate_name}. Supported gates are: X, Hadamard, CNOT, CZ, Y, Z, S, T, Rx, Ry, Rz, Identity."
            )
        gate = None
        print(gate_name)
        match gate_name:
            case "X":
                gate = X(qubits=target_qubits)
            case "h":
                gate = Hadamard(qubits=target_qubits)
            case "cx":
                if len(target_qubits) != 2:
                    raise ValueError("CNOT gate requires exactly 2 target qubits.")
                gate = CNOT(
                    control_qubit=target_qubits[0], target_qubit=target_qubits[1]
                )
            case "CZ":
                if len(target_qubits) != 2:
                    raise ValueError("CZ gate requires exactly 2 target qubits.")
                gate = CZ(qubits=target_qubits)
            case "Y":
                gate = Y(qubits=target_qubits)
            case "Z":
                gate = Z(qubits=target_qubits)
            case "S":
                gate = S(qubits=target_qubits)
            case "T":
                gate = T(qubits=target_qubits)
            case "Rx":
                gate = Rx(qubits=target_qubits, theta=params.get("theta", 0))
            case "Ry":
                gate = Ry(qubits=target_qubits, theta=params.get("theta", 0))
            case "Rz":
                gate = Rz(qubits=target_qubits, theta=params.get("theta", 0))
            case "Identity":
                gate = Identity(qubits=target_qubits)

        self.gates.append(gate)

    def __repr__(self):
        return f"QuantumCircuit(qubits={self.qubits}, gates={self.gates})"

    def print_summary(self):
        """Print the number of qubits and gates in the circuit."""
        print(f"Number of qubits: {len(self.qubits)}")
        print(f"Number of gates: {len(self.gates)}")

    def print_each_gate_class_name(self):
        """Print the class names of each gate in the circuit."""
        for gate in self.gates:
            print("Gate class name: ", gate.__class__.__name__)
            print("Gate qubits: ", gate.qubits)
            # print(f"Gate: {gate['name']}, Qubits: {gate['qubits']}, Params: {gate['params']}")
