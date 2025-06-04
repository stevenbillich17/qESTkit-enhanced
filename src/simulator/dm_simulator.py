import numpy as np
from typing import List, Dict, Union, Optional
from qestkit_simulator import QuantumSimulator
from typing import Any


class DensityMatrixSimulator(QuantumSimulator):
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.density_matrix = np.zeros((2**num_qubits, 2**num_qubits), dtype=complex)
        self.reset()

    def reset(self):
        # Initialize the density matrix to the |0...0⟩ state
        self.density_matrix = np.zeros(
            (2**self.num_qubits, 2**self.num_qubits), dtype=complex
        )
        self.density_matrix[0, 0] = 1.0

    def get_num_qubits(self) -> int:
        return self.num_qubits

    def apply_gate(
        self,
        gate_name: str,
        targets: Union[int, List[int]],
        controls: Optional[Union[int, List[int]]] = None,
        params: Optional[List[float]] = None,
    ):
        # Example implementation for single-qubit gates
        if isinstance(targets, int):
            targets = [targets]

        gate_matrix = self._get_gate_matrix(gate_name, params)
        for target in targets:
            self._apply_single_qubit_gate(gate_matrix, target)

    def apply_custom_gate(
        self,
        gate_matrix: np.ndarray,
        targets: Union[int, List[int]],
        controls: Optional[Union[int, List[int]]] = None,
    ):
        # Apply a custom gate matrix to the density matrix
        if isinstance(targets, int):
            targets = [targets]

        for target in targets:
            self._apply_single_qubit_gate(gate_matrix, target)

    def run(self, circuit: Any, shots: int = 1024) -> Dict[str, int]:
        # Simulate measurement outcomes
        probabilities = np.real(np.diag(self.density_matrix))
        outcomes = {
            bin(i)[2:].zfill(self.num_qubits): 0 for i in range(2**self.num_qubits)
        }

        for _ in range(shots):
            sampled_state = np.random.choice(len(probabilities), p=probabilities)
            outcomes[bin(sampled_state)[2:].zfill(self.num_qubits)] += 1

        return outcomes

    def calculate_expectation_value(
        self, observable: np.ndarray, state_vector: np.ndarray
    ) -> float:
        # Calculate expectation value using the density matrix
        return np.real(np.trace(np.dot(self.density_matrix, observable)))

    def _get_gate_matrix(
        self, gate_name: str, params: Optional[List[float]]
    ) -> np.ndarray:
        # Define gate matrices (example: Pauli-X, Hadamard)
        if gate_name == "x":
            return np.array([[0, 1], [1, 0]], dtype=complex)
        elif gate_name == "h":
            return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        else:
            raise ValueError(f"Unsupported gate: {gate_name}")

    def _apply_single_qubit_gate(self, gate_matrix: np.ndarray, target: int):
        # Apply a single-qubit gate to the density matrix
        full_gate = np.eye(2**self.num_qubits, dtype=complex)
        for i in range(2**self.num_qubits):
            if (i >> target) & 1 == 0:
                full_gate[i, i] = gate_matrix[0, 0]
                full_gate[i, i + (1 << target)] = gate_matrix[0, 1]
            else:
                full_gate[i, i] = gate_matrix[1, 1]
                full_gate[i, i - (1 << target)] = gate_matrix[1, 0]

        self.density_matrix = full_gate @ self.density_matrix @ full_gate.T.conj()
