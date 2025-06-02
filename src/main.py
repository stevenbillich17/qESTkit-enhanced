from loader import Loader

if __name__ == "__main__":
    # Example usage of the Loader class to load a QASM2 circuit
    # Adjust the path to your QASM2 file as necessary
    circuit = Loader.load_qasm2("qasm2/ghz.qasm")
    circuit.print_summary()
    circuit.print_each_gate_class_name()
