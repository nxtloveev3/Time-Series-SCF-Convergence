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
2. [Repository Structure](#repository-structure)
3. [Usage](#usage)
    * [1. Feature Extraction](#1-feature-extraction)
    * [2. Adaptive Recovery in PySCF](#2-deployment-with-beta-rst)
4. [Citation](#citation)
5. [Acknowledgments](#acknowledgments)

## Data Availability

**Raw Outputs**
The raw output files for the doublet anion calculations (TeraChem) are hosted at: [DOI].

**Dataset Access**
All datasets used for training, validation, and benchmarking the models are available in the [`feature_sets`](./Data/feature_sets/).

**Pre-trained Models**
The optimized model weights for models trained on iSmall-train, iMedium-train, and iLarge-train, are stored with corresponding min-max scalar under the [`Models`](./Models/) directory.

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
We recommend using Conda (or Mamba) to install the required dependencies and ensure version compatibility.

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
Next, install the custom PySCF with adaptive level shifting:
```bash
pip install git+https://github.com/nxtloveev3/pyscf_Adaptive_Level_Shifting.git
```
Because `pip` do not automatically transfer large binary files like the pretrained model during a GitHub source installation you have to copy the pre-trained model into your Conda environment's PySCF directory:
```bash
# 1. Ask Python where PySCF is installed
PYSCF_PATH=$(python -c "import os, pyscf; print(os.path.dirname(pyscf.__file__))")

# 2. Copy the model into the scf module folder
cp ./models/iMedium_model.pkl $PYSCF_PATH/scf/
```
Now you can run the scripts to generate the time-series feature set and perform adaptive level shifting UHF calculations in PySCF.

## 1. Feature Extraction
The `feature_extraction.py` script transforms raw [`sample_outputs`](./Data/sample_outputs/) (from TeraChem) into a structured dataset of **153 statistical descriptors**. These features captures the SCF progression within a 10-iteration window, metrics include:
* **Central Tendency:** Median and Mean.
* **Volatility:** Standard deviation (SD) and Rolling SD.
* **Trends:** Slope and Autocorrelation.

### Execution
Navigate to the [`Scripts`](./Scripts/) directory and run the extraction:
```bash
cd scripts
python feature_extraction.py`
```

## 2. Deployment with Beta-RST

The `adaptive_shifting_pyscf.py` script serves as the deployment-ready [PySCF](https://github.com/nxtloveev3/pyscf_Adaptive_Level_Shifting) implementation of the **$\beta$-RST** logic. It acts as an automated "supervisor" for PySCF calculations, using the pre-trained GBC to predict and mitigate convergence failures in real-time.

### Execution
Navigate to the [`Scripts`](./Scripts/) directory and run the extraction:
```bash
cd scripts
python ./scripts/adaptive_shifting_pyscf.py \
    --molecule_file "./Data/sample_molecules/sample.xyz" \
    --molecule_name "test_molecule_01" \
    --log_root "./logs" \
    --max_attempts 10
```

### Implement Our Model with C/C++ Inference 
For high-performance integration into quanutm chemistry packages (e.g., C, C++, wrappers), we provide a workflow to export the trained GBC to the **ONNX (Open Neural Network Exchange)** format. 

This allows the $\beta$-RST logic to be implemented natively using the [ONNX Runtime (ORT)](https://onnxruntime.ai/) without requiring a Python interpreter at runtime.

To export our model you can use the provided `to_onnx` utility in the [`src`](./src/) library to convert your `.pkl` weights into a `.onnx` binary.

```python
from src.heuristic_implementation import to_onnx

# Converts the 'iMedium' model to ONNX
to_onnx(file_path="./Models/iMedium_model.pkl", model_size="iSmall", num_features=6)
```
Once the model is converted, you can implement the initialization and probability inference functions by following the reference code in [`src`](./src/c_implementation.cpp)

---

## Citation
Lechen Dong, Fang Liu. Accelerating Quantum Chemistry Automation: Early Detection and Recovery of SCF Convergence Failure via Time Series Feature Extraction. ChemRxiv. 30 March 2026.
DOI: https://doi.org/10.26434/chemrxiv.15001181/v2

---

## Acknowledgement
L.D. acknowledges joint financial support from the DOE Office of Science Early Career Research Program Award, managed by the DOE BES CPIMS program under Award No. DE- SC0025345, and the Research Corporation for Science Advancement via the Cottrell Scholar Award #CS-CSA-2024-099. This research used the resources of the National Energy Research Scientific Computing Center, a DOE Office of Science User Facility supported by the Office of Science of the U.S. Department of Energy under Contract No. DE-AC02-05CH11231 using NERSC award BES-ERCAP0033060.
