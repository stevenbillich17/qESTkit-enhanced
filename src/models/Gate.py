import numpy as np
from src.models.QuantumObject import QuantumObject
from src.models.NoiseChannel import NoiseChannel


class Gate(QuantumObject):
    """
    Base class for quantum gates.

    Attributes:
        name (str): Name of the gate (e.g., 'X', 'H', 'CNOT').
        qubits (list): List of qubit indices this gate acts on.
        matrix (numpy.ndarray, optional): The matrix representation of the gate (2x2 for single-qubit gates, 4x4 for two-qubit gates, etc.).
    """

    def __init__(self, name, qubits, matrix=None):
        """
        Initializes a quantum gate.

        Args:
            name (str): The name of the gate.
            qubits (list): A list of integer qubit indices that the gate acts on.
            matrix (numpy.ndarray, optional): The matrix representation of the gate.  Defaults to None.
        """
        super().__init__(name)
        self.qubits = qubits
        self.matrix = matrix

    def apply(self, quantum_state, simulator_type="state_vector"):
        """
        Applies the gate to the given quantum state.  The implementation depends
        on the type of simulator being used (state vector, density matrix, tensor network).

        Args:
            quantum_state: The quantum state to be transformed.  This can be a state vector (NumPy array),
                            a density matrix (NumPy array), or a tensor network (object).
            simulator_type (str, optional):  The type of simulator being used.  Valid values are "state_vector",
                                            "density_matrix", and "tensor_network".  Defaults to "state_vector".

        Returns:
            The transformed quantum state.

        Raises:
            ValueError: If an invalid simulator type is specified.
            NotImplementedError: If the apply method is not implemented for the given simulator type.
        """
        if simulator_type == "state_vector":
            return self._apply_state_vector(quantum_state)
        elif simulator_type == "density_matrix":
            return self._apply_density_matrix(quantum_state)
        elif simulator_type == "tensor_network":
            return self._apply_tensor_network(quantum_state)
        else:
            raise ValueError(
                f"Invalid simulator type: {simulator_type}. Must be 'state_vector', 'density_matrix', or 'tensor_network'."
            )

    def _apply_state_vector(self, state_vector):
        """
        Applies the gate to a state vector.  Override this method in subclasses
        if a more efficient implementation is possible.

        Args:
            state_vector (numpy.ndarray): The state vector.

        Returns:
            numpy.ndarray: The transformed state vector.
        """
        num_qubits = int(np.log2(len(state_vector)))
        self.validate(num_qubits)  # Make sure the gate is valid for this system
        operator = self.get_operator(num_qubits)
        return operator @ state_vector

    def _apply_density_matrix(self, density_matrix):
        """
        Applies the gate to a density matrix. Override this method in subclasses
        for specific density matrix implementations.

        Args:
            density_matrix (numpy.ndarray): The density matrix.

        Returns:
            numpy.ndarray: The transformed density matrix.
        """
        num_qubits = (
            int(np.log2(density_matrix.shape[0])) // 1
        )  # Corrected to find integer log base 2 for density matrices
        self.validate(num_qubits)
        operator = self.get_operator(num_qubits)
        operator_dagger = np.conjugate(operator).transpose()
        return operator @ density_matrix @ operator_dagger

    def _apply_tensor_network(self, tensor_network):
        """
        Applies the gate to a tensor network representation.

        Args:
            tensor_network: The tensor network object. The specific type of the tensor network is not specified here.

        Returns:
            The transformed tensor network.
        """
        raise NotImplementedError("Tensor network implementation not yet available.")

    def validate(self, num_qubits):
        """
        Validates the gate's target qubits against the total number of qubits.

        Args:
            num_qubits (int): Total number of qubits in the quantum system.

        Raises:
            ValueError: If any target qubit index is invalid, or the number of qubits acted upon by the gate is incorrect.
        """
        if any(q >= num_qubits or q < 0 for q in self.qubits):
            raise ValueError(
                f"Invalid qubit indices {self.qubits} for a system with {num_qubits} qubits."
            )

        # Add a check for the correct number of qubits in the gate's definition
        expected_matrix_size = 2 ** len(self.qubits)
        if self.matrix is not None and self.matrix.shape != (
            expected_matrix_size,
            expected_matrix_size,
        ):
            raise ValueError(
                f"Gate {self.name} matrix has incorrect dimensions. Expected {expected_matrix_size}x{expected_matrix_size}, but got {self.matrix.shape}."
            )

    def get_operator(self, num_qubits):
        """
        Constructs the full operator for the quantum system. This implementation uses kronecker products.
        Override this method in subclasses for optimized implementations, especially for tensor networks.

        Args:
            num_qubits (int): Total number of qubits in the quantum system.

        Returns:
            numpy.ndarray: A matrix representing the gate operator for the full system.
        """
        if self.matrix is None:
            raise ValueError("Gate matrix is not defined.")

        identity = np.eye(2, dtype=complex)
        target_qubits = sorted(self.qubits)  # Ensure qubits are in increasing order
        num_target_qubits = len(target_qubits)
        all_qubits = list(range(num_qubits))

        # Find qubits that are acted upon by the gate and unaffected qubits
        affected_qubits = target_qubits
        unaffected_qubits = [q for q in all_qubits if q not in affected_qubits]

        # Initialize the operator to the gate's matrix
        operator = self.matrix

        # Build the full operator by kroneckering the identity matrix for each unaffected qubit
        for _ in range(num_qubits - num_target_qubits):
            operator = np.kron(identity, operator)

        # Construct a permutation to map the operator's qubit order to the standard qubit order.
        permutation = []
        index_affected = 0
        index_unaffected = 0
        for _ in range(num_qubits):
            if index_unaffected < len(unaffected_qubits) and unaffected_qubits[
                index_unaffected
            ] < min(affected_qubits, default=float("inf")):
                permutation.append(unaffected_qubits[index_unaffected])
                index_unaffected += 1
            else:
                permutation.append(affected_qubits[index_affected])
                index_affected += 1
        permute = np.argsort(permutation)

        # Permute the operator
        original_shape = (2,) * num_qubits
        permuted_axes = tuple(permute)
        operator = operator.reshape(original_shape + original_shape)
        operator = np.moveaxis(
            operator, range(num_qubits), range(num_qubits, 2 * num_qubits)
        )  # Swapping order
        operator = np.moveaxis(
            operator,
            range(num_qubits, 2 * num_qubits),
            [i + num_qubits for i in permute],
        )
        operator = operator.reshape((2**num_qubits, 2**num_qubits))

        return operator

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, qubits={self.qubits})"


# Example Usage
if __name__ == "__main__":
    # Define some example gates (you'll need to define the matrices)
    X_matrix = np.array([[0, 1], [1, 0]], dtype=complex)
    H_matrix = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
    CNOT_matrix = np.array(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex
    )

    x_gate = Gate(name="X", qubits=[0], matrix=X_matrix)
    h_gate = Gate(name="H", qubits=[0], matrix=H_matrix)
    cnot_gate = Gate(
        name="CNOT", qubits=[0, 1], matrix=CNOT_matrix
    )  # Control qubit 0, target qubit 1

    # Example with state vector simulator
    num_qubits = 2
    initial_state = np.array([1, 0, 0, 0], dtype=complex)  # Initial state |00>

    try:
        h_gate.validate(num_qubits)
        cnot_gate.validate(num_qubits)
        final_state = cnot_gate.apply(
            h_gate.apply(initial_state, simulator_type="state_vector"),
            simulator_type="state_vector",
        )
        print("Final State (State Vector):", final_state)

        # Example with density matrix simulator
        initial_density_matrix = np.outer(
            initial_state, np.conjugate(initial_state)
        )  # |00><00|
        final_density_matrix = cnot_gate.apply(
            h_gate.apply(initial_density_matrix, simulator_type="density_matrix"),
            simulator_type="density_matrix",
        )
        print("Final Density Matrix:", final_density_matrix)

    except ValueError as e:
        print(f"Error: {e}")
    except NotImplementedError as e:
        print(f"Not implemented: {e}")

    # Example NoiseChannel (Placeholder - needs implementation)
    # depolarizing_channel = NoiseChannel(name="DepolarizingChannel", strength=0.01)
    # print(depolarizing_channel)
    # To properly use the depolarizing channel, you need to define:
    # 1.  A _apply_state_vector method for it (or _apply_density_matrix, _apply_tensor_network)
    # 2.  Code to apply the noise according to the depolarization model.  This is non-trivial.
