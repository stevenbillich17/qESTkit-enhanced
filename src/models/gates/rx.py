import numpy as np
from .gate import Gate


class Rx(Gate):
    def __init__(self, theta, qubits=None):
        """
        Initialize the Rx gate (rotation around X-axis).

        :param theta: Rotation angle in radians.
        :param qubits: Optional, indices of qubits this gate acts on.
        """
        super().__init__(name="Rx", qubits=qubits)
        self.theta = theta

    def apply(self, simulator_context, **kwargs):
        """
        Apply the Rx gate using the provided simulator context.
        The actual implementation is handled by the simulator.

        :param simulator_context: The context of the simulator.
        :param kwargs: Additional arguments specific to the simulator or gate.
        :return: The modified simulator context.
        """
        pass
