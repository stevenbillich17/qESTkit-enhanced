import qiskit

class Loader:
    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def load_qasm2(circuit_file:str) -> QuantumCircuit:
        pass