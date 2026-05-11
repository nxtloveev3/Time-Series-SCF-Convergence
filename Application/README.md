# Deployment Guide: Integrating Adaptive Level-Shifting into Quantum Chemistry Software
Welcome to the `application` directory. This folder contains the deployment-ready scripts, pre-trained models, and C/C++ reference implementations necessary to integrate our automated SCF recovery approach into your prefered quantum chemistry packages.

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
to_onnx(file_path="./Models/iMedium_model.pkl", model_size="iMedium", num_features=6)
```
Once the model is converted, you can implement the initialization and probability inference functions by following the reference code in [`src`](./src/c_implementation.cpp)

---
