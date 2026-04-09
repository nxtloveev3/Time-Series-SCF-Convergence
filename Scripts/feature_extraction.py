import sys
import pandas as pd
from pathlib import Path
import numpy as np

# 1. Path Management
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent 
src_path = str(project_root / "src")

# Add 'src' to system path if it's not already there to allow custom imports
if src_path not in sys.path:
    sys.path.append(src_path)

# 2. Custom Imports
from extractors import get_data_set, get_feat_names, extract_features

# 3. Data Loading
data_path = str(script_dir.parent / "Data/sample_outputs")
sample_dat, fails = get_data_set(data_path)

# 4. Process Time Signals
# Drops the last two rows (iteration count and spin) and selects iteration 1 through 10 ([:, 1:11]) for each sample
time_signals = [np.array(dat[:-2])[:, 1:11] for dat in sample_dat]

# 5. Extract Features
ts_features = extract_features(
    time_signals, 
    alpha_homo_lumo_idx=(5, 6), 
    beta_homo_lumo_idx=(11, 12)
)

# 6. Define Labels
raw_labels = [
    'diis', 'En', 'dE', 
    r'$\alpha$_HOMO_2', r'$\alpha$_HOMO_1', r'$\alpha$_HOMO',  
    r'$\alpha$_LUMO', r'$\alpha$_LUMO_1', r'$\alpha$_LUMO_2', 
    r'$\beta$_HOMO_2', r'$\beta$_HOMO_1', r'$\beta$_HOMO', 
    r'$\beta$_LUMO', r'$\beta$_LUMO_1', r'$\beta$_LUMO_2', 
    r'$\alpha$_gap', r'$\beta$_gap'
]
ts_feature_labels = get_feat_names(raw_labels)

# 7. Construct Final Dataset
feature_set = pd.DataFrame(ts_features, columns=ts_feature_labels)

feature_set.to_csv('sample_ts_feature_set.csv')