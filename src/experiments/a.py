"""
Minimally reproduces Fig. 2.
"""

import matplotlib.pyplot as plt
import numpy as np

from typing import Tuple
from qht import ExecuteQHT, CircuitInfo

def analytics(N: int = 128, h: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
    """
    Samples test function and analytic Hilbert transform pair used in Sec. (4)(A).
    """
    x = np.linspace(-N // 2 * h, (N // 2 - 1) * h, N)
    f = np.sin(x) / (1 + x**4)
    g = (np.exp(-1 / np.sqrt(2)) * np.cos(1 / np.sqrt(2)) + np.exp(-1 / np.sqrt(2)) * np.sin(1 / np.sqrt(2)) * x**2 - np.cos(x)) / (1 + x**4)
    return f, g

def cht(signal: np.ndarray) -> np.ndarray:
    """
    Classical discrete Hilbert transform implementation using the FFT.
    """
    H = np.fft.ifft(np.fft.fft(signal) * (-1j * np.sign(np.fft.fftfreq(len(signal)))))
    return H / np.linalg.norm(H)

def fidelity(psi: np.ndarray, phi: np.ndarray) -> float:
    """
    Computes the fidelity between two pure quantum states.
    """
    return np.abs(np.vdot(psi, phi))**2

if __name__ == '__main__':
    n = 10
    N = 2**n

    f, g = analytics(N, 0.01)
    signal = f / np.linalg.norm(f)
    
    analytic_result = g / np.linalg.norm(g)
    classical_result = cht(signal)
    quantum_result = ExecuteQHT(signal, n, 1, True)
    CircuitInfo(n, 1)

    print(f"Fidelity (Quantum vs. Classical): {fidelity(quantum_result, classical_result)}")
    print(f"Fidelity (Quantum vs. Analytic): {fidelity(quantum_result, analytic_result)}")

    x = np.arange(N)
    fig, (res_ax, err_ax) = plt.subplots(2, 1, figsize=(10, 10), tight_layout=True)

    res_ax.plot(x, np.real(quantum_result), label='Quantum Result', color='blue')
    res_ax.plot(x, np.real(classical_result), label='Classical Result', color='orange', linestyle='-.')
    res_ax.plot(x, np.real(analytic_result), label='Analytic Result', color='green')
    res_ax.set(title="Hilbert Transform Results", xlabel="Sample", ylabel="Amplitude")
    res_ax.legend()

    err_ax.plot(x, np.abs(quantum_result - analytic_result), label='Quantum Error', color='blue')
    err_ax.plot(x, np.abs(classical_result - analytic_result), label='Classical Error', color='orange', linestyle='-.')
    err_ax.set(title="Error Comparison", xlabel="Sample", ylabel="Absolute Error")
    err_ax.legend()

    plt.show()