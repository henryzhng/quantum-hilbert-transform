"""
Minimally reproduces Fig. 3.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from qht import ExecuteQHT, CircuitInfo

def amp(signal: np.ndarray) -> np.ndarray:
    """
    Classical analytic signal implementation using the FFT.
    """
    H = np.fft.ifft(np.fft.fft(signal) * (-1j * np.sign(np.fft.fftfreq(len(signal)))))
    return np.abs(H * 1j + signal)

if __name__ == '__main__':
    n = 15
    N = 2**n

    data = pd.read_csv('data/currents.csv', header=2)
    time = data.iloc[:, 0].values[:N]
    signal = data.iloc[:, 1].values[:N] / np.linalg.norm(data.iloc[:, 1].values[:N])

    classical_result = amp(signal)
    quantum_result = np.abs(np.real(ExecuteQHT(signal, n, 1, True)) * 1j + signal)
    CircuitInfo(n, 1)

    x = np.arange(N)
    fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)

    ax.plot(x, signal, label='Signal', color='green')
    ax.plot(x, quantum_result, label='Quantum Instantaneous Amplitude', color='blue')
    ax.plot(x, classical_result, label='Classical Instantaneous Amplitude', color='orange', linestyle='--')
    ax.set(title="Instantaneous Amplitude Results", xlabel="Sample", ylabel="Amplitude")
    ax.legend()
    plt.show()