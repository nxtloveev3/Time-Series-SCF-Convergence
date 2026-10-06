# Running SCF Feature Extraction and Adaptive Recovery

This directory contains sample inputs, trained classifiers, and research implementations for SCF failure prediction and beta-level-shift restart (beta-RST). The adaptive calculation example requires the project's modified PySCF fork. The C/C++ file is an integration snippet, not a standalone executable.

## Environment Setup

Start at the repository root:

```bash
git clone https://github.com/nxtloveev3/Time-Series-SCF-Convergence.git
cd Time-Series-SCF-Convergence
conda env create -f Application/requirements.yml
conda activate adap_scf_env
```

The environment includes dependencies for feature extraction, the notebooks, and ONNX tools. The following examples use **`Application/` as the working directory**:

```bash
cd Application
```

Keep this working directory for each command below. Directory names such as `Scripts`, `Models`, and `Data` are case-sensitive.

## 1. Extract Features from Bundled Outputs

```bash
python Scripts/feature_extraction.py
```

The script reads [`Data/sample_outputs/`](./Data/sample_outputs/) and writes `sample_ts_feature_set.csv` in your current directory. It generates 153 descriptors for each of the 10 bundled outputs: 17 signals, including two frontier-orbital gaps, with nine statistics per signal. The CSV also contains an index column.

This example does not run new quantum chemistry calculations. The features describe a 10-iteration window using statistics such as median, standard deviation, slope, fluctuation range, extrema count, and autocorrelation.

## 2. Install the Adaptive PySCF Fork

The modified SCF driver is pinned to a specific revision in [`requirements-pyscf.txt`](./requirements-pyscf.txt):

```bash
python -m pip install -r requirements-pyscf.txt
```

This installs PySCF from source and requires Git, a C/C++ compiler, and the native build dependencies supported by PySCF. Its Python build requirements include CMake. Installation can take longer than the base environment setup.

Copy the classifier into the installed fork's SCF directory, where its driver expects to find it:

```bash
SCF_PACKAGE_DIR=$(python -c 'from pathlib import Path; import pyscf; print(Path(pyscf.__file__).resolve().parent / "scf")')
cp Models/iMedium_model.pkl "$SCF_PACKAGE_DIR/iMedium_model.pkl"
```

The upstream PySCF release does not implement this fork's `dynamic_ls` behavior. Use the pinned fork for the adaptive example.

## 3. Run a Bundled Molecule

```bash
python Scripts/adaptive_shifting_pyscf.py \
    --molecule_file Data/sample_molecules/dsgdb9nsd_000970.xyz \
    --molecule_name dsgdb9nsd_000970 \
    --log_root logs \
    --max_attempts 10
```

The example performs UHF/6-31++G** calculations for a doublet anion with an hcore initial guess. It reports restart information in the terminal and writes a detailed log to `logs/dsgdb9nsd_000970_beta_RST_log.txt`. Runtime and convergence depend on the molecule and hardware; check the log for the final convergence outcome.

## 4. Export a Classifier to ONNX

After installing the fork above, run this from `Application/`:

```bash
python - <<'PY'
from src.heuristic_implementation import to_onnx

output_path = to_onnx(output_dir="exports", model_size="iMedium", num_features=6)
print(output_path)
PY
```

The function loads `Models/iMedium_model.pkl`, checks the feature count, creates the output directory, and writes `exports/gbc_iMedium.onnx`. `output_dir` is a **directory**, not the path to the input pickle. The model identifier can also be `iSmall` or `iLarge`.

The exported model accepts a float32 tensor named `x` with shape `[batch_size, 6]` and exposes class labels and probabilities. It exports the classifier only: callers must supply the same six selected features, in the same order and with the same preprocessing used during training. The 153-column extraction output cannot be passed directly to this model.

[`src/c_implementation.cpp`](./src/c_implementation.cpp) shows ONNX Runtime session initialization and inference calls. To integrate it into another program, supply the ONNX Runtime headers and libraries, the surrounding state declarations and error-handling macro, and the feature-preprocessing code. Validate predicted probabilities against the Python classifier before using an integration for calculations.
