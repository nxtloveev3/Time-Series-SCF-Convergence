import sys
import os
import argparse
from pathlib import Path

# Path Management
script_dir = Path(__file__).parent.resolve()
src_path = str(script_dir.parent / "src")

if src_path not in sys.path:
    sys.path.append(src_path)

from heuristic_implementation import adaptive_PySCF

def main():
    parser = argparse.ArgumentParser(
        description="Deploy adaptive PySCF heuristic for automated open shell SCF convergence."
    )
    
    # Required arguments
    parser.add_argument("--molecule_file", required=True, type=str, help="Path to the molecular geometry file (.xyz)")
    parser.add_argument("--molecule_name", required=True, type=str, help="Identifier for the molecule")
    parser.add_argument("--log_root", required=True, type=str, help="Directory to save the log files")
    
    # Optional argument with a default value
    parser.add_argument("--max_attempts", type=int, default=10, 
                        help="Maximum number of beta shift attempts (default: 10)")

    args = parser.parse_args()

    os.makedirs(args.log_root, exist_ok=True)

    print(f"Starting adaptive SCF for {args.molecule_name}...")
    
    # Execute the heuristic
    attempts, restarting_cycles, alpha_shift, beta_shift = adaptive_PySCF(
        args.molecule_file, 
        args.molecule_name, 
        args.log_root, 
        args.max_attempts
    )

    # Output summary
    print("\n--- Heuristic Execution Summary ---")
    print(f"Molecule:          {args.molecule_name}")
    print(f"Total Attempts:    {attempts}")
    print(f"Restarting Cycles: {restarting_cycles}")
    print(f"Final Alpha Shift: {alpha_shift:.2f}")
    print(f"Final Beta Shift:  {beta_shift:.2f}")
    print("-----------------------------------")

if __name__ == "__main__":
    main()
