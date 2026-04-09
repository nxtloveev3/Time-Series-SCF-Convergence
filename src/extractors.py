import re
import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.signal import find_peaks

def extract_hf_information(file_input: str, verbose: bool=False):
    """
    Parses a Hartree Fock single point energy calculation output file and returns a dataframe of desired descriptors' histories.

    Args:
        file_input (str): The path to the output file.
        verbose (bool): If True, prints lines that are ignored during parsing.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted descriptors for each iteration.
    """
    
    # 1. Helper function and Regex setup
    def namedRe(name, respec, before='none', after='require'): 
        ws = {'none': r'', 'allow': r'\s*', 'require': r'\s+'}
        return ws[before] + "(?P<" + name + ">" + respec + ")" + ws[after]

    reFloat = r"-?\+?\d+\.\d+"
    
    float_fields = [
        "Energy_change", "alphaHOMO_2", "alphaHOMO_1", "alphaHOMO",
        "alphaLUMO", "alphaLUMO_1", "alphaLUMO_2", "betaHOMO_2", "betaHOMO_1",
        "betaHOMO", "betaLUMO", "betaLUMO_1", "betaLUMO_2", "J", "K", "LA",
        "DFT", "Energy", "Time"
    ]

    energy_line_hf = (
        r'\|' + 
        namedRe("Iter", r"\d+", before="allow") + 
        namedRe("DIIS_Error", reFloat, before="allow", after="allow") +
        "".join(namedRe(name, reFloat, after="allow") for name in float_fields) + 
        r'\n'
    )

    energy_line_hfRe = re.compile(energy_line_hf)

    # 2. Map regex-safe names back to desired column names
    key_map = {
        "alphaHOMO_2": "alphaHOMO-2", "alphaHOMO_1": "alphaHOMO-1",
        "alphaLUMO_1": "alphaLUMO+1", "alphaLUMO_2": "alphaLUMO+2",
        "betaHOMO_2": "betaHOMO-2",   "betaHOMO_1": "betaHOMO-1",
        "betaLUMO_1": "betaLUMO+1",   "betaLUMO_2": "betaLUMO+2",
    }

    result = []
    
    with open(file_input, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if match := energy_line_hfRe.match(line):
            result.append({
                key_map.get(k, k): int(v) if k == "Iter" else float(v)
                for k, v in match.groupdict().items()
            })
        elif verbose:
            print("Ignoring this line:", line.strip()) 

    # 4. Return as a parsed pandas DataFrame
    return pd.DataFrame(result)

def get_data_set(folder_path: str, verbose: bool=False) -> pd.DataFrame:
    """
    Parses all files in the specified folder and extracts the desired descriptors into a list of lists.
    
    Args:
        folder_path (str): The path to the folder containing the output files.
        verbose (bool): If True, prints lines that are ignored during parsing.

    Returns:
        list: A list of lists, where each inner list contains the extracted descriptors for a molecule.
        list: A list of file paths that failed to parse.
    """
    data = []
    failed = []
    
    # Define the exact column order we want to extract
    target_cols = [
        'DIIS_Error', 'Energy', 'Energy_change', 
        'alphaHOMO-2', 'alphaHOMO-1', 'alphaHOMO', 'alphaLUMO', 'alphaLUMO+1', 'alphaLUMO+2',
        'betaHOMO-2', 'betaHOMO-1', 'betaHOMO', 'betaLUMO', 'betaLUMO+1', 'betaLUMO+2'
    ]

    folder = Path(folder_path)
    
    # Get all files sorted, ignoring hidden files like .DS_Store
    mols = sorted(f for f in folder.iterdir() if f.is_file() and not f.name.startswith('.'))

    for file_path in mols:
        try:
            # 1. Parse the DataFrame
            df = extract_hf_information(file_path, verbose)

            if df.empty:
                failed.append(str(file_path))
                continue

            # Read all lines once
            with open(file_path, 'r') as f:
                lines = f.readlines()
 
            # 2. Extract all 15 columns at once into a list of lists 
            molecule = df[target_cols].values.T.tolist()
            
            # 3. Append iteration count
            molecule.append(len(df))
            
            # 4. Search for SPIN S-SQUARED and append to molecule's information
            spin_val = None
            for line in lines:
                if line.startswith('SPIN S-SQUARED:'):
                    spin_val = line.replace('SPIN S-SQUARED: ', '').replace('(exact: 0.75)', '').strip()
                    break
            
            molecule.append(spin_val)
            data.append(molecule)

        except Exception as e:
            failed.append(str(file_path))
                    
    return data, failed

def calculate_slope(series: np.ndarray) -> float:
    """
    Calculate the linear trend (slope) of a time series using least squares.
    
    Args:
        series (np.ndarray): 1D array representing the time series.
        
    Returns:
        float: The slope of the linear regression line.
    """
    x = np.arange(len(series)).reshape(-1, 1)
    reg = LinearRegression().fit(x, series)
    return reg.coef_[0]

def calculate_fluctuation(series: np.ndarray, window: int = 5) -> tuple[float, float, int]:
    """
    Calculate fluctuation metrics: range, rolling standard deviation, and extrema count.
    
    Args:
        series (np.ndarray): 1D array representing the time series.
        window (int): Window size for the rolling standard deviation.
        
    Returns:
        tuple: (range_value, mean_rolling_std, num_peaks_valleys)
    """
    range_value = np.max(series) - np.min(series)
    rolling_std = pd.Series(series).rolling(window=window).std().mean()  # Rolling std with a window of 5
    peaks, _ = find_peaks(series)
    valleys, _ = find_peaks(-series)
    num_peaks_valleys = len(peaks) + len(valleys)
    
    return range_value, rolling_std, num_peaks_valleys

def calculate_trend_vs_fluctuation_ratio(slope: float, fluctuation_std: float) -> float:
    """
    Calculate the ratio of trend (slope) to fluctuation (standard deviation).
    
    Args:
        slope (float): The slope of the time series.
        fluctuation_std (float): The standard deviation of the fluctuations.

    Returns:
        float: The ratio of slope to fluctuation standard deviation, or 0 if fluctuation_std is zero.
    """
    return slope / fluctuation_std if fluctuation_std != 0 else 0.0

def calculate_change_in_trend(series: np.ndarray) -> float:
    """
    Calculate the change in trend between the first and second halves of the series.
    
    Args:
        series (np.ndarray): 1D array representing the time series.
    
    Returns:
        float: The difference in slope between the second half and the first half of the series.
    """
    mid_point = len(series) // 2
    
    # Handle cases where the series is too short to split
    if mid_point < 2:
        return 0.0
        
    slope_first_half = calculate_slope(series[:mid_point])
    slope_second_half = calculate_slope(series[mid_point:])
    
    return slope_second_half - slope_first_half

def calculate_autocorrelation(series: np.ndarray) -> float:
    """
    Calculate lag-1 autocorrelation for the time series.
    
    Args:
        series (np.ndarray): 1D array representing the time series.
        
    Returns:
        float: The lag-1 autocorrelation value.
    """
    if len(series) < 2:
        return 0.0
        
    # np.corrcoef is computationally lighter than statsmodels.tsa.stattools.acf for a single lag
    corr_matrix = np.corrcoef(series[:-1], series[1:])
    
    # Handle flatline series where correlation would result in NaN
    if np.isnan(corr_matrix[0, 1]):
        return 0.0
        
    return corr_matrix[0, 1]

def gen_features(series: list | np.ndarray) -> list[float]:
    """
    Generate a comprehensive set of time-series features.
    
    Args:
        series (list or np.ndarray): The input time series data.
        
    Returns:
        list[float]: A list containing [median, standev, slope, fluctuation_range, 
                     fluctuation_std, num_peaks_valleys, trend_vs_fluctuation_ratio, 
                     change_in_trend, autocorrelation].
    """
    # Cast to NumPy array immediately to ensure mathematical operations (like -series) work
    series = np.asarray(series, dtype=float)
    
    # Basic statistical features
    median = np.median(series)
    standev = np.std(series)

    # Advanced time-series features
    slope = calculate_slope(series)
    fluctuation_range, fluctuation_std, num_peaks_valleys = calculate_fluctuation(series)
    trend_vs_fluctuation_ratio = calculate_trend_vs_fluctuation_ratio(slope, fluctuation_std)
    change_in_trend = calculate_change_in_trend(series)
    autocorrelation = calculate_autocorrelation(series)
    
    return [
        median, 
        standev, 
        slope, 
        fluctuation_range, 
        fluctuation_std, 
        float(num_peaks_valleys), 
        trend_vs_fluctuation_ratio, 
        change_in_trend, 
        autocorrelation
    ]

def get_feat_names(series: list) -> np.ndarray:
    """
    Generate feature names for the extracted features based on the input series names.

    Args:
        series (list): A list of base names for the time series (e.g., ['Energy', 'DIIS_Error']).

    Returns:
        np.ndarray: An array of feature names corresponding to the generated features for each series.
    """
    labels = []
    for name in series: #name + r'_$\bar{x}$',
        feature_names = [name + r'_Med', name + r'_$\sigma$', name + '_Slope', name + '_Range', name + r'_$\sigma_{rolling}$', name + '_#_Peaks', name + r'_$R_{trend/fluct}$', name + r'_$\Delta$_Slope', name + '_ACF']
        labels.extend(feature_names)
    return np.array(labels)

import numpy as np

def extract_features(data, alpha_homo_lumo_idx=(5, 6), beta_homo_lumo_idx=(11, 12)):
    """
    Extracts statistical features from molecular time-series data.
    
    Args:
        data (list or np.ndarray): The dataset containing multiple molecular samples.
        alpha_homo_lumo_idx (tuple): Row indices for (alphaHOMO, alphaLUMO).
        beta_homo_lumo_idx (tuple): Row indices for (betaHOMO, betaLUMO).
        
    Returns:
        np.ndarray: A 2D array of computed feature vectors for all samples.
    """
    features = []
    
    for sample in data:
        
        feature_vector = []
        
        # 1. Dynamically iterate through EVERY row in the sample
        for feat in sample:
            feature_vector.extend(gen_features(feat))
            
        # 2. Calculate the energy gaps dynamically based on provided indices
        # LUMO (index 1) minus HOMO (index 0)
        alpha_gap = sample[alpha_homo_lumo_idx[1]] - sample[alpha_homo_lumo_idx[0]]
        beta_gap = sample[beta_homo_lumo_idx[1]] - sample[beta_homo_lumo_idx[0]]
        
        # 3. Add the gap features
        feature_vector.extend(gen_features(alpha_gap))
        feature_vector.extend(gen_features(beta_gap))
        
        features.append(feature_vector)
        
    return np.array(features)