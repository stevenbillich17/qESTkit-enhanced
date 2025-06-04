import numpy as np
from abc import ABC, abstractmethod


class Gate(ABC):
    def __init__(self, name, qubits=None):
        """
        Base class for quantum gates.

        :param name: Name of the gate (e.g., 'X', 'H').
        :param qubits: List of qubit indices this gate acts on.
        """
        self.name = name
        self.qubits = qubits if qubits is not None else []
        # Matrix removed, will be handled by simulators

    @abstractmethod
    def apply(self, simulator_context, **kwargs):
        """
        Apply the gate using the provided simulator context.
        This method must be implemented by specific gate types in conjunction with simulator logic.

        :param simulator_context: The context of the simulator (e.g., state vector, density matrix).
        :param kwargs: Additional arguments specific to the simulator or gate.
        :return: The modified simulator context.
        """
        pass

    def validate(self, num_qubits):
        """
        Validate the gate's target qubits against the total number of qubits.

        :param num_qubits: Total number of qubits in the quantum system.
        :raises ValueError: If any target qubit index is invalid.
        """
        if any(q >= num_qubits or q < 0 for q in self.qubits):
            raise ValueError(
                f"Invalid qubit indices {self.qubits} for a system with {num_qubits} qubits."
            )

    # get_operator removed, will be handled by simulators

    def __repr__(self):
        return f"Gate(name={self.name}, qubits={self.qubits})"
