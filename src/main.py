import qiskit
from qiskit import QuantumCircuit

QuantumCircuit.from_qasm_file("qasm2/ghz.qasm").draw(output="mpl", scale=0.5, style={"name": "iqx"}).savefig("qasm2/ghz.png")