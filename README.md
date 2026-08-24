# Early Detection and Recovery of SCF Convergence Failures in Automated Quantum Chemistry Workflows via Time-Series Learning
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Paper](https://img.shields.io/badge/Paper-ChemRxiv-red.svg)](https://chemrxiv.org/doi/full/10.26434/chemrxiv.15001181/v3)

## Overview
Self-consistent field (SCF) convergence failures remain a major bottleneck in high-throughput quantum chemistry, particularly for open-shell systems. `Time-Series-SCF-Convergence` pioneers a novel paradigm by treating the iterative SCF procedure as a sequential time-series problem. This modular, data-efficient pipeline lays the essential groundwork for fully autonomous SCF fine-tuning by accurately predicting convergence outcomes and proactively correcting difficult calculations.

By treating the electronic descriptors in the early SCF iterations as a time-series signal, our lightweight Gradient-Boosted Classifier (GBC) predicts convergence failure before computational resources are wasted. These calculations are then automatically intercepted and rescued using a Bayesian optimization-motivated proof-of-concept intervention policy $\beta$-level-shift restart ($\beta$-RST) heuristic.

### Key Features
* **Transferable Implementation:** The six core input features required by the model (e.g., median orbital energy of $\alpha$-HOMO, total energy oscillation count) are universally accessible by all quantum chemistry calcualtion softwares, allowing for integration across all major packages.
* **High Data Efficiency:** Achieves >94% predictive accuracy on massive hold-out sets (55k molecules) after training on less than 10% of the dataset (10k molecules).
* **Automated Recovery:** Our monitoring model triggers SCF restarts, with the selected spin-channel shift escalated in successive attempts. This approach successfully reduced overall SCF iterations by over 248,355 steps across 1,200 calculations, with 53.9% rescue of genuinely difficult cases and 96.3% easy-case convergence..

---

## Table of Contents
1. [Data Availability](#data-availability)
2. [Citation](#citation)
3. [Acknowledgments](#acknowledgments)

## Data Availability
**Extracted SCF Iteraction Information for All Domains**
The raw output from the doublet anion calculations (TeraChem) for all calculation settings are hosted at Figshare: https://doi.org/10.6084/m9.figshare.32227395.

**Gradient Boosting Classifier Training and Evaluation**
All datasets used for training, validation, and testing the gradient boosting classifiers are also available at Figshare: https://doi.org/10.6084/m9.figshare.32227395.

**Pre-trained Models**
The optimized model weights for models trained on iSmall-train, iMedium-train, and iLarge-train, are stored with corresponding min-max scalar under the [`Models`](./Application/Models/) directory.

**Reproduce Paper Findings**
To replicate the main text figures, supplementary information (SI) figures, and the performance evaluations presented in our study, we have provided a suite of interactive Jupyter notebooks. 

All scripts necessary to recreate these findings are located in the [`sample_notebooks/`](./sample_notebooks/) directory. Please ensure you have downloaded and extracted the `notebook_data.zip` archive from Figshare into the `notebook_data/` folder before executing these notebooks.

**notebook data**
All the preprocessed data that is useful for reproducing the paper findings via the jupyter notebooks can be found under the [`notebook_data`](./notebook_data/) directory.

---

## Citation
Lechen Dong, Fang Liu. Accelerating Quantum Chemistry Automation: Early Detection and Recovery of SCF Convergence Failure via Time Series Feature Extraction. ChemRxiv. 30 March 2026.
DOI: https://doi.org/10.26434/chemrxiv.15001181/v2

---

## Acknowledgement
L.D. acknowledges joint financial support from the DOE Office of Science Early Career Research Program Award, managed by the DOE BES CPIMS program under Award No. DE- SC0025345, and the Research Corporation for Science Advancement via the Cottrell Scholar Award #CS-CSA-2024-099. This research used the resources of the National Energy Research Scientific Computing Center, a DOE Office of Science User Facility supported by the Office of Science of the U.S. Department of Energy under Contract No. DE-AC02-05CH11231 using NERSC award BES-ERCAP0033060.
