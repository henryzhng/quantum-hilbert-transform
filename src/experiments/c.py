"""
Minimally reproduces Fig. 4.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from qht import ExecuteQHT, CircuitInfo

if __name__ == '__main__':
    n = 10
    N = 2**n

    image = np.array(Image.open('data/chessboard.png').convert('L'))
    image = image[:N, :N] / np.linalg.norm(image[:N, :N])

    quantum_result = ExecuteQHT(image.flatten(), n, 2, True).reshape((N, N))
    CircuitInfo(n, 2)

    plt.imshow(np.abs(quantum_result), cmap='gray')
    plt.title("Quantum Hilbert Transform Result")
    plt.colorbar(label='Amplitude')
    plt.show()
