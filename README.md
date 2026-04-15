# Time-Series-SCF-Convergence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Paper](https://img.shields.io/badge/Paper-ChemRxiv-red.svg)](https://doi.org/10.26434/chemrxiv.15001181/v2) **Accelerating Quantum Chemistry Automation: Early Detection and Recovery of SCF Convergence Failure via Time Series Feature Extraction**

## Overview
Self-consistent field (SCF) convergence failures remain a major bottleneck in high-throughput quantum chemistry, particularly for open-shell systems. `Time-Series-SCF-Convergence` provides a software-agnostic, data-efficient machine learning pipeline to proactively detect and correct these failures. 

By treating the electronic descriptors in the early SCF iterations as a time-series signal, our lightweight Gradient-Boosted Classifier (GBC) predicts convergence failure before computational resources are wasted. These calculations are then automatically intercepted and rescued using a physically grounded $\beta$-level-shift restart ($\beta$-RST) heuristic derived from Bayesian optimization.

### Key Features
* **Software-Agnostic Implementation:** The six core input features required by the model (e.g., median orbital energy of $\alpha$-HOMO, total energy oscillation count) are universally accessible, allowing for effortless integration across all major quantum chemistry packages.
* **High Data Efficiency:** Achieves >94% predictive accuracy on massive hold-out sets (55k molecules) after training on less than 10% of the dataset (10k molecules).
* **Automated Recovery:** Dynamically applies targeted $\beta$-spin level shifts to bypass near-degeneracy traps, reducing overall SCF iterations by over 460,000 steps across diverse benchmarks.

---

## Table of Contents
1. [Data Availability](#data-availability)
2. [Repository Structure](#repository-structure)
3. [Usage](#usage)
    * [1. Feature Extraction](#1-feature-extraction)
    * [2. Adaptive Recovery in PySCF](#2-deployment-with-beta-rst)
4. [Citation](#citation)
5. [Acknowledgments](#acknowledgments)

## Data Availability

---

## Repository Structure
```bash
Time-Series-SCF-Convergence/
├── data/                              # Data directory
│   ├── sample_outputs/                # Raw sample SCF output logs (TeraChem)
│   └── features/                      # Extracted time-series features sets for iSmall, iMedium, and iLarge
├── models/                            # Pre-trained GBC weights and scalers
├── src/                               # Adaptive level shifting workflow modules
│   ├── extractors/                    # Log parsing and time-series feature generation
│   └── heuristics_implementation/     # Packaging adpative level shifting approach to be used in QC softwares
├── scripts/                           # Executable scripts for the adaptive level shifting workflow
│   ├── 01_features_extraction.py      # Demonstration of feature extraction process for the sample SCF output logs
│   └── 02_adaptive_shifting_pyscf.py  # Demonstration of running beta-RST heuristic with PySCF
├── requirements.yml                   # Environment dependencies
└── README.md
```
---

## Usage
We recommend using Conda (or Mamba) to install the required dependencies and ensure version compatibility:
First, clone the repository and navigate into it:
```bash
git clone https://github.com/yourusername/Time-Series-SCF-Convergence.git
cd Time-Series-SCF-Convergence
```
Next, build and activate the Conda environment using the provided YAML file:
```bash
conda env create -f requirements.yml
conda activate adap_scf_env
```

---

## Citation
Lechen Dong, Fang Liu. Accelerating Quantum Chemistry Automation: Early Detection and Recovery of SCF Convergence Failure via Time Series Feature Extraction. ChemRxiv. 30 March 2026.
DOI: https://doi.org/10.26434/chemrxiv.15001181/v2

---

## Acknowledgement
L.D. acknowledges joint financial support from the DOE Office of Science Early Career Research Program Award, managed by the DOE BES CPIMS program under Award No. DE- SC0025345, and the Research Corporation for Science Advancement via the Cottrell Scholar Award #CS-CSA-2024-099. This research used the resources of the National Energy Research Scientific Computing Center, a DOE Office of Science User Facility supported by the Office of Science of the U.S. Department of Energy under Contract No. DE-AC02-05CH11231 using NERSC award BES-ERCAP0033060.
