# Early Detection and Recovery of SCF Convergence Failures in Automated Quantum Chemistry Workflows via Time-Series Learning
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Published in JCTC](https://img.shields.io/badge/Published_in-JCTC-00539B?style=flat-square)](https://doi.org/10.1021/acs.jctc.6c00928)

## Overview

Self-consistent field (SCF) convergence failures can make high-throughput quantum chemistry calculations expensive, particularly for open-shell systems. This repository accompanies our study of time-series learning for early detection and recovery of SCF convergence failures. It contains feature-extraction code, trained classifiers, an adaptive restart example, and notebooks for inspecting the paper's results.

The gradient-boosted classifier (GBC) uses electronic descriptors from the first 10 SCF iterations to predict convergence outcomes. A Bayesian-optimization-informed beta-level-shift restart ($\beta$-RST) heuristic then attempts to recover predicted failures by adjusting the level shift and restarting the calculation.

### Key Features

* **Quantum chemistry and machine learning:** Extracts time-series features from TeraChem output and includes a recovery example using a modified PySCF implementation. Other packages require matching descriptor extraction, feature order, and preprocessing; compatibility must be validated for each integration.
* **Data-efficient prediction:** Achieved 94.8% accuracy on 53,885 held-out doublet anionic QM9 molecules using 10,000 training examples.
* **Automated recovery:** Saved 248,355 SCF iterations across 1,200 calculations and rescued 53.9% of difficult cases in the study. These are study results, not expected outcomes for every new molecule or package.

## Start Here

For a quick research overview, open [`sample_notebooks/figures.ipynb`](./sample_notebooks/figures.ipynb). Its saved outputs show the paper's main figures. To run a small example locally:

```bash
git clone https://github.com/nxtloveev3/Time-Series-SCF-Convergence.git
cd Time-Series-SCF-Convergence
conda env create -f Application/requirements.yml
conda activate adap_scf_env
python Application/Scripts/feature_extraction.py
```

The extraction script reads the bundled TeraChem outputs and writes `sample_ts_feature_set.csv` in your current directory. The expected result is 10 rows and 153 descriptor columns, plus the CSV index column. This step does not launch new quantum chemistry calculations or require the custom PySCF installation.

To inspect the main figures interactively:

```bash
cd sample_notebooks
jupyter lab figures.ipynb
```

Run the import cell and the two code cells under **Figure 1** to generate the SCF iteration histogram and `Figure_1.pdf`. The notebook expects its working directory to be `sample_notebooks/`; it reads the bundled files in `../notebook_data/`. Later sections include additional analyses and may take longer to run.

See the [application guide](./Application/README.md) for the custom PySCF installation, a molecular calculation example, and ONNX export.

### Repository Map

| Location | Contents |
|---|---|
| [`Application/Scripts/`](./Application/Scripts/) | Feature-extraction and adaptive PySCF entry points |
| [`Application/src/`](./Application/src/) | Parsing, feature generation, restart logic, ONNX export, and a C/C++ integration snippet |
| [`Application/Models/`](./Application/Models/) | Saved GBC models and associated scalers |
| [`Application/Data/`](./Application/Data/) | Sample molecular geometries and TeraChem outputs |
| [`sample_notebooks/`](./sample_notebooks/) | Main figures, supplementary analyses, and Figshare data usage |
| [`notebook_data/`](./notebook_data/) | Bundled inputs for the figure notebooks |
| [`Figures/`](./Figures/) | Exported research figures |

## Table of Contents

1. [Start Here](#start-here)
2. [Data Availability](#data-availability)
3. [Citation](#citation)
4. [Acknowledgments](#acknowledgments)

## Data Availability

**Extracted SCF Iteration Information for All Domains**

The raw output from the doublet anion calculations (TeraChem) for all calculation settings is hosted at Figshare: https://doi.org/10.6084/m9.figshare.32227395.

**Gradient Boosting Classifier Training and Evaluation**

Datasets used for training, validation, and testing the gradient boosting classifiers are also available at Figshare: https://doi.org/10.6084/m9.figshare.32227395.

**Pre-trained Models**

The models trained on iSmall-train, iMedium-train, and iLarge-train are stored with their corresponding min-max scalers under the [`Models`](./Application/Models/) directory.

**Reproduce Paper Findings**

The notebooks are in [`sample_notebooks/`](./sample_notebooks/). Inputs for the figure notebooks are already included in [`notebook_data/`](./notebook_data/), so the Figure 1 example above does not require a Figshare download. The [`figshare_usage.ipynb`](./sample_notebooks/figshare_usage.ipynb) notebook demonstrates training and evaluation using the larger Figshare datasets; download those inputs separately and set its data paths for your machine.

The Conda environment includes plotting, Jupyter, PyTorch, and GPyTorch dependencies used by the notebooks. The notebooks retain the study's training and plotting code; reproducing every analysis is more computationally demanding than the quick-start example.

### Figure Data Requirements

| Notebook sections | Inputs |
|---|---|
| Main Figures 1–10 | Included in `notebook_data/` |
| SI Figures S4 and S7–S11 | Included in `notebook_data/` |
| SI Figure S1 bottom schematic | Training-set size constants in the style/setup cell; no external data |
| SI Figure S1 main panel | Additional `dataset_test_no_norm.pkl` |
| SI Figure S2 | Additional `Data/feature_sets/iSmall_train.csv` |
| SI Figures S3 and S5 | Additional `pre_selection_features.pkl` |
| SI Figure S6 | Additional `rnn_data_iMedium.pkl` and `rolling_window_info.pkl`, alongside bundled inputs |

Without the additional data, run the SI import and style/setup cells, then only the supported sections above. Running every SI cell sequentially stops at the first missing input. Paths are relative to the `sample_notebooks/` working directory.

## Citation

Lechen Dong and Fang Liu. **Early Detection and Recovery of SCF Convergence Failures in Automated Quantum Chemistry Workflows via Time-Series Learning.** *Journal of Chemical Theory and Computation*, 2026. https://doi.org/10.1021/acs.jctc.6c00928

Earlier preprint: https://doi.org/10.26434/chemrxiv.15001181/v2

## Acknowledgments

L.D. acknowledges joint financial support from the DOE Office of Science Early Career Research Program Award, managed by the DOE BES CPIMS program under Award No. DE- SC0025345, and the Research Corporation for Science Advancement via the Cottrell Scholar Award #CS-CSA-2024-099. This research used the resources of the National Energy Research Scientific Computing Center, a DOE Office of Science User Facility supported by the Office of Science of the U.S. Department of Energy under Contract No. DE-AC02-05CH11231 using NERSC award BES-ERCAP0033060.
