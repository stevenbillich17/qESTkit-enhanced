class QuantumObject:
    """
    Base class for quantum objects that interact with the simulator (gates, noise models, etc.).

    Attributes:
        name (str): Name of the object (e.g., 'CNOT', 'DepolarizingChannel').
    """

    def __init__(self, name):
        self.name = name

    def validate(self, num_qubits):
        """
        Validate the object against the total number of qubits in the system.
        This method should be overridden by subclasses to perform specific validation checks.

        Args:
            num_qubits (int): Total number of qubits in the quantum system.

        Raises:
            NotImplementedError: If called on the base class directly.
        """
        raise NotImplementedError("Validate method must be implemented by the subclass.")

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"
