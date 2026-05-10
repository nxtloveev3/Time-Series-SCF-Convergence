# Time-Series-SCF-Convergence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Paper](https://img.shields.io/badge/Paper-ChemRxiv-red.svg)](https://doi.org/10.26434/chemrxiv.15001181/v2) **Accelerating Quantum Chemistry Automation: Early Detection and Recovery of SCF Convergence Failure via Time Series Feature Extraction**

## Overview
Self-consistent field (SCF) convergence failures remain a major bottleneck in high-throughput quantum chemistry, particularly for open-shell systems. `Time-Series-SCF-Convergence` pioneers a novel paradigm by treating the iterative SCF procedure as a sequential time-series problem. This software-agnostic, data-efficient pipeline lays the essential groundwork for fully autonomous SCF fine-tuning by accurately predicting convergence outcomes and proactively correcting difficult calculations.

By treating the electronic descriptors in the early SCF iterations as a time-series signal, our lightweight Gradient-Boosted Classifier (GBC) predicts convergence failure before computational resources are wasted. These calculations are then automatically intercepted and rescued using a physically grounded $\beta$-level-shift restart ($\beta$-RST) heuristic derived from Bayesian optimization.

### Key Features
* **Software-Agnostic Implementation:** The six core input features required by the model (e.g., median orbital energy of $\alpha$-HOMO, total energy oscillation count) are universally accessible, allowing for effortless integration across all major quantum chemistry packages.
* **High Data Efficiency:** Achieves >94% predictive accuracy on massive hold-out sets (55k molecules) after training on less than 10% of the dataset (10k molecules).
* **Automated Recovery:** Dynamically applies targeted $\beta$-spin level shifts to bypass near-degeneracy traps, reducing overall SCF iterations by over 460,000 steps across diverse benchmarks.

---

## Table of Contents
1. [Data Availability](#data-availability)
2. [Citation](#citation)
3. [Acknowledgments](#acknowledgments)

## Data Availability

**Extracted SCF Iteraction Information for All Domains**
The raw output from the doublet anion calculations (TeraChem) for all calculation settings are hosted at Figshare: https://doi.org/10.6084/m9.figshare.32227395.

**Gradient Boosting Classifier Training and Evaluation**
All datasets used for training, validation, and testing the models are also available at Figshare: https://doi.org/10.6084/m9.figshare.32227395.

**notebook data**
All the preprocessed data that is useful for reproducing the paper findings via the jupyter notebooks can be found under the [`notebook_data`](./notebook_data/) directory.

**Pre-trained Models**
The optimized model weights for models trained on iSmall-train, iMedium-train, and iLarge-train, are stored with corresponding min-max scalar under the [`Models`](./Application/Models/) directory.

---

## Citation
Lechen Dong, Fang Liu. Accelerating Quantum Chemistry Automation: Early Detection and Recovery of SCF Convergence Failure via Time Series Feature Extraction. ChemRxiv. 30 March 2026.
DOI: https://doi.org/10.26434/chemrxiv.15001181/v2

---

## Acknowledgement
L.D. acknowledges joint financial support from the DOE Office of Science Early Career Research Program Award, managed by the DOE BES CPIMS program under Award No. DE- SC0025345, and the Research Corporation for Science Advancement via the Cottrell Scholar Award #CS-CSA-2024-099. This research used the resources of the National Energy Research Scientific Computing Center, a DOE Office of Science User Facility supported by the Office of Science of the U.S. Department of Energy under Contract No. DE-AC02-05CH11231 using NERSC award BES-ERCAP0033060.
