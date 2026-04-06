# Time-Series-SCF-Convergence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
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
1. [Installation](#installation)
2. [Data Availability](#data-availability)
3. [Repository Structure](#repository-structure)
4. [Usage](#usage)
    * [1. Feature Extraction](#1-feature-extraction)
    * [2. Model Training](#2-model-training)
    * [3. Adaptive Recovery ($\beta$-RST)](#3-adaptive-recovery--rst)
5. [Citation](#citation)
6. [Acknowledgments](#acknowledgments)

---

## Installation

Clone the repository and install the required dependencies. We recommend using a `conda` virtual environment.

```bash
git clone [https://github.com/YourUsername/TS-ML-SCF-Convergence.git](https://github.com/YourUsername/TS-ML-SCF-Convergence.git)
cd TS-ML-SCF-Convergence
conda create -n ts-scf python=3.9
conda activate ts-scf
pip install -r requirements.txt
