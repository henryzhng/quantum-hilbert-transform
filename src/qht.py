"""
Reference implementation for the quantum Hilbert transform.
"""

import numpy as np
import itertools

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator, Aer
from qiskit.compiler import transpile

def BuildQHT(n: int, d: int, state: np.ndarray | None = None) -> QuantumCircuit:
    """
    Constructs a d-dimensional quantum Hilbert transform on d * n data qubits
    plus d target ancillas and one classical bit.

    Parameters
    ----------
    n     : Number of qubits per register.
    d     : Hilbert transform dimension (number of registers)
    state : Initial quantum state to be transformed. If provided, it will be used as the initial state of the circuit.
            If None (default), the circuit will start with all qubits in |0⟩.

    Returns
    -------
    QuantumCircuit
        The quantum circuit implementing the d-dimensional Hilbert transform.
    """
    if n < 1 or d < 1:
        raise ValueError("n and d must be positive.")
    
    data = [QuantumRegister(n, name=f"r{i}") for i in range(d)]
    target = QuantumRegister(d, name="targ")
    creg = ClassicalRegister(d, name="c")
    qc = QuantumCircuit(*data, target, creg)

    if state is not None:
        if len(state) != 2**(n * d):
            raise ValueError(f"State length {len(state)} does not match {2**(n * d)} for n={n}, d={d}.")
        if not np.isclose(np.linalg.norm(state), 1):
            raise ValueError("Input state must be normalised.")
        qc.initialize(state, range(n * d))
    
    for register in data:
        qc.append(QFT(num_qubits=n), register)
    qc.barrier()

    for i, register in enumerate(data):
        qc.mcx(list(register), target[i], ctrl_state="0" * n, mode="noancilla")
        qc.measure(target[i], creg[i])
    qc.barrier()

    for register in data:
        qc.z(register[-1])
    qc.barrier()

    for register in data:
        qc.append(QFT(num_qubits=n, inverse=True), register)
    qc.barrier()

    return qc    

def BuildDynamicQHT(n: int, d: int, ancilla: bool = True, state: np.ndarray | None = None) -> QuantumCircuit:
    """

    Constructs a d-dimensional quantum Hilbert transform on d * n data qubits
    plus one target ancilla, one ancilla for decomposing multi-controlled X gates (optional), and one classical bit, using dynamic circuits to measure
    and reset the target qubit mid-circuit.

    Parameters
    ----------
    n      : Number of qubits per register.
    d      : Hilbert transform dimension (number of registers)
    state  : Initial quantum state to be transformed. If provided, it will be used as the initial state of the circuit.
             If None (default), the circuit will start with all qubits in |0⟩.
    ancilla: Whether to include an ancilla qubit for decomposing multi-controlled X gates.

    Returns
    -------
    QuantumCircuit
        The quantum circuit implementing the d-dimensional Hilbert transform.
    """
    if n < 1 or d < 1:
        raise ValueError("n and d must be positive.")

    data = [QuantumRegister(n, name=f"r{i}") for i in range(d)]
    target = QuantumRegister(1, name="targ")
    anc = QuantumRegister(1, name="anc") if ancilla else None
    creg = ClassicalRegister(1, name="c")

    qc = QuantumCircuit(*data, target, anc if ancilla else [], creg)

    if state is not None:
        if len(state) != 2**(n * d):
            raise ValueError(f"State length {len(state)} does not match {2**(n * d)} for n={n}, d={d}.")
        if not np.isclose(np.linalg.norm(state), 1):
            raise ValueError("Input state must be normalised.")
        qc.initialize(state, range(n * d))

    for register in data:
        qc.append(QFT(num_qubits=n), register)
    qc.barrier()

    for register in enumerate(data):
        qc.mcx(list(register[1]), target[0], ctrl_state="0" * n, mode="recursion", ancilla_qubits=anc[:]) if ancilla else qc.mcx(list(register[1]), target[0], ctrl_state="0" * n, mode="noancilla")
        qc.measure(target[0], creg[0])
        qc.reset(target[0])
    qc.barrier()

    for register in data:
        qc.z(register[-1])
    qc.barrier()

    for register in data:
        qc.append(QFT(num_qubits=n, inverse=True), register)
    qc.barrier()

    return qc

def ExecuteQHT(signal: np.ndarray, n: int, d: int = 1, dynamic: bool = True) -> np.ndarray:
    """
    Execute the QHT circuit and return the (normalised)
    transformed statevector slice corresponding to the data register.

    Parameters
    ----------
    signal : Real-valued input samples (power of two length, already normalised).
    n      : Number of qubits per register.
    d      : Hilbert transform dimension (number of registers)
    dynamic: Whether to use the dynamic circuit version.

    Returns
    -------
    np.ndarray
        Normalised statevector corresponding to the Hilbert transform of the input signal.
    """
    qc = BuildDynamicQHT(n, d, True, signal) if dynamic else BuildQHT(n, d, signal)

    qc = transpile(qc, AerSimulator())
    counts, state = None, None

    if dynamic:
        while counts != {'0': 1}:
            result = Aer.get_backend('statevector_simulator').run(qc, shots=1).result()
            counts = result.get_counts()
            state = np.asarray(result.get_statevector() * 1j)[:2**(n * d)]
    else:
        while counts != {'0' * d: 1}:
            result = Aer.get_backend('statevector_simulator').run(qc, shots=1).result()
            counts = result.get_counts()
            state = np.asarray(result.get_statevector() * 1j)[:2**(n * d)]

    return state

def CircuitInfo(n: int, d: int, dynamic: bool = True) -> None:
    """
    Pretty-print the input QuantumCircuit and its gate counts in the [u, cx] basis.
    """
    qc = BuildDynamicQHT(n, d, True) if dynamic else BuildQHT(n, d)

    print(f"QHT circuit for n={n}, d={d}:\n")
    print(qc)

    qc = transpile(qc, basis_gates=["u", "cx"], optimization_level=3)
    counts = qc.count_ops()
    counts.pop("barrier", None)
    print(f"{qc.size()} gates: {counts}.")

    return None