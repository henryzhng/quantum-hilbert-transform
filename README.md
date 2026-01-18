## Quantum Hilbert Transform

This repository accompanies the paper

H. Zhang and J. Li, “Efficient Quantum Circuits for the Hilbert Transform,” IEEE Signal Processing Letters, 2026, doi: [10.1109/LSP.2026.3654893](https://doi.org/10.1109/LSP.2026.3654893)

and contains:

1. Qiskit implementations of the quantum Hilbert transform in `src/qht.py`;
2. Scripts to reproduce the figures and benchmarks from the paper in `src/experiments`.

## Usage

With Python ≥ 3.10, clone the repository:
```bash
git clone https://github.com/henryzhng/quantum-hilbert-transform.git
cd quantum-hilbert-transform
pip install -e .
```

Then reproduce the experiments (Figs. 2 to 4) by running:

```bash
python src/experiments/a.py
python src/experiments/b.py
python src/experiments/c.py
```

Or, for information on the quantum circuits used, refer to functions in `src/qht.py`. There are both dynamic and static circuit implementations.

## Citation
    
If you use this work, please cite:

```bibtex
@article{Zhang2026,
  title = {Efficient Quantum Circuits for the Hilbert Transform},
  ISSN = {1558-2361},
  DOI = {10.1109/LSP.2026.3654893},
  journal = {IEEE Signal Processing Letters},
  author = {Zhang, Henry and Li, Joseph},
  year = {2026},
  pages = {1–5}
}
```

The code is licensed under the [MIT License](LICENSE).
