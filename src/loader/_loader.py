import qiskit
from src.dtos import QuantumCircuit

class Loader:
    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def load_qasm2(circuit_file:str) -> QuantumCircuit:
        qs_circuit = qiskit.qasm2.load(circuit_file)
        qc = QuantumCircuit()
        for instruction in qs_circuit.data:
            continue
        # TODO parse circuit into own datastructure
        return qc

    @staticmethod
    def load_qasm3(circuit_file:str) -> QuantumCircuit:
        # Placeholder for future implementation
        raise NotImplementedError("QASM3 loading not implemented yet.")

    @staticmethod
    def load_ir(circuit_file:str):
        # Placeholder for future implementation
        raise NotImplementedError("IR loading not implemented yet.")
