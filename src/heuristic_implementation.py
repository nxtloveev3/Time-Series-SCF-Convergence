import os
import pickle
import pyscf
from pyscf import lib
from pyscf.scf import uhf
from pathlib import Path
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnx

def to_onnx(file_path, model_size="iSmall", num_features=6):
    """
    Converts a trained scikit-learn model to ONNX format for native C/C++ inference.

    Args: file_path (str): Path to save the ONNX model.
          model_size (str): Identifier for the model size (e.g., "iSmall", "iMedium", "iLarge").
          num_features (int): Number of features expected by the model.

    Returns: None. Saves the ONNX model to provided file_path.
    """
    model_folder = Path(__file__).resolve().parent.parent / "models"
    model_path = model_folder / f"{model_size}_model.pkl"
    
    with open(model_path, "rb") as f:
        gbc = pickle.load(f)

    initial_types = [("x", FloatTensorType([None, num_features]))]
    onnx_model = convert_sklearn(gbc, initial_types=initial_types, options={"zipmap": False})

    output_filename = f"gbc_{model_size}.onnx"
    output_filepath = os.path.join(file_path, output_filename)
    onnx.save_model(onnx_model, output_filename)
    print(f"Successfully exported ONNX model to {output_filename}")


def extract_molecule_PySCF(file_path, basis='6-31++G**'):
    """
    Parses a geometry file, cleans scientific notation, and builds a PySCF Molecule object.\
    
    Args: file_path (str): Path to the geometry file.
          basis (str): Basis set to use for the molecule.

    returns: PySCF Molecule object with the specified geometry and basis set.
    """
    formatted_lines = []
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 4 and parts[0].isalpha() and parts[0].lower() != "gdb":
                atom = parts[0].upper()
                coords = [c.replace('*^', 'e') for c in parts[1:4]]
                formatted_lines.append(f"{atom} {' '.join(coords)}")

    formatted_content = '\n'.join(formatted_lines)
    return pyscf.M(atom=formatted_content, basis=basis)


def adaptive_PySCF(molecule_path, molecule_name, log_root, max_attempts=10):
    """
    Executes UHF calculations, iteratively increasing beta level shift upon convergence failure.

    Args: molecule_path (str): Path to the molecule geometry file.
          molecule_name (str): Identifier for the molecule, used in log file naming.
          log_root (str): Directory to save the log files.
          max_attempts (int): Maximum number of attempts of restart with level-shifting.

    returns: Tuple containing (number of attempts, total restart cycles, final alpha shift, final beta shift).
    """
    mol = extract_molecule_PySCF(molecule_path, '6-31++G**')
    mol.charge = -1
    mol.spin = 1
    mol.build()

    alpha_shift = 0.0
    beta_shift = 0.0
    restart_cycle = 0
    log_file = os.path.join(log_root, f"{molecule_name}_beta_RST_log.txt")

    for attempt in range(max_attempts):
        mf = pyscf.scf.UHF(mol)
        mf.init_guess = 'hcore'
        mf.dynamic_ls = True
        mf.diis_space = 10
        mf.conv_tol = 9e-10
        mf.conv_tol_grad = 3e-5
        mf.max_cycle = 2000
        mf.level_shift = (alpha_shift, beta_shift)
        mf.verbose = lib.logger.DEBUG

        mode = 'w' if attempt == 0 else 'a'
        with open(log_file, mode) as log_handle:
            mf.stdout = log_handle
            
            try:
                mf.kernel()
                
                if mf.converged:
                    print(f"Convergence successful for {molecule_name} | a={alpha_shift}, b={beta_shift}")
                    return attempt + 1, restart_cycle, alpha_shift, beta_shift
                else:
                    print(f"Attempt {attempt + 1} failed for {molecule_name}. Retrying with beta_shift={beta_shift + 0.1:.1f}")
                    restart_cycle += mf.max_cycle
                    beta_shift += 0.1
                    
            except RuntimeError as e:
                msg = str(e)
                if "Cycle=" in msg:
                    try:
                        restart_cycle += int(msg.split("Cycle=")[1].split()[0])
                    except (IndexError, ValueError):
                        pass
                print(f"RuntimeError on attempt {attempt + 1} for {molecule_name}. Retrying.")
                beta_shift += 0.1

    # Fallback Execution
    print(f"All {max_attempts} attempts failed for {molecule_name}. Running final fallback.")
    mf = pyscf.scf.UHF(mol)
    mf.init_guess = 'hcore'
    mf.dynamic_ls = False 
    mf.diis_space = 10
    mf.conv_tol = 9e-10
    mf.conv_tol_grad = 3e-5
    mf.max_cycle = 2000
    mf.level_shift = (alpha_shift, beta_shift)
    mf.verbose = lib.logger.DEBUG

    with open(log_file, 'a') as log_handle:
        mf.stdout = log_handle
        mf.kernel()

    return max_attempts, restart_cycle, alpha_shift, beta_shift