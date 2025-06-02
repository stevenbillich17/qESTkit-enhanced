import numpy as np
from .gate import Gate

class Hadamard(Gate):
    def __init__(self, qubits=None):
        """
        Initialize the Hadamard gate.

        :param qubits: Optional, indices of qubits this gate acts on.
        """
        super().__init__(name='H', qubits=qubits)

    def apply(self, simulator_context, **kwargs):
        """
        Apply the Hadamard gate using the provided simulator context.
        The actual implementation is handled by the simulator.

        :param simulator_context: The context of the simulator.
        :param kwargs: Additional arguments specific to the simulator or gate.
        :return: The modified simulator context.
        """
        pass

