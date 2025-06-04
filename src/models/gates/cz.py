import numpy as np
from .gate import Gate


class CZ(Gate):
    def __init__(self, qubits=None):
        """
        Initialize the Controlled-Z gate.

        :param qubits: Indices of qubits this gate acts on. Should contain exactly two qubits: [control, target].
        """
        if qubits is None or len(qubits) != 2:
            raise ValueError("CZ gate requires exactly two qubits: [control, target].")
        super().__init__(name="CZ", qubits=qubits)

    def apply(self, simulator_context, **kwargs):
        """
        Apply the CZ gate using the provided simulator context.
        The actual implementation is handled by the simulator.

        :param simulator_context: The context of the simulator.
        :param kwargs: Additional arguments specific to the simulator or gate.
        :return: The modified simulator context.
        """
        pass
