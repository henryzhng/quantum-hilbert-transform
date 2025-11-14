# Quantum Hilbert Transform

This repository accompanies the paper

> Zhang, H., Li, J. **“Efficient Quantum Circuits for the Hilbert Transform”**, _Journal_, 2025. DOI: [10.0000/placeholder](https://doi.org/10.0000/placeholder)

and contains:

1. A Qiskit implementation of the quantum Hilbert transform in `src/qht.py`
2. Scripts to reproduce the figures and benchmarks from the paper in `src/experiments/`

## Usage

(Requires Python 3.10.0 or higher, packages listed in `pyproject.toml`).

Clone the repository locally:

```bash
git clone https://github.com/henryzhng/quantum-hilbert-transform.git
cd quantum-hilbert-transform
pip install -e .
```

Then, replicate the experiments (Figs. 2–4) by running:

```bash
python src/experiments/a.py
python src/experiments/b.py
python src/experiments/c.py
```

Or, for information on the quantum circuits used, refer to the `BuildQHT, CircuitInfo` classes in `src/qht.py`.

## Citation
    
If you use this work, please cite:

```
@article{Zhang2025QHT,
    title={Efficient Quantum Circuits for the Hilbert Transform},
    author={Henry Zhang and Joseph Li},
    journal={Journal},
    volume={},
    pages={},
    year={2025},
    doi={10.0000/placeholder}
}
```

This project is licensed under the [MIT License](LICENSE).
